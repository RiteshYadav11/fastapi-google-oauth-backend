from fastapi import APIRouter, Depends, Request, HTTPException, Header
from authlib.integrations.starlette_client import OAuth, OAuthError
import os
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..utils import create_access_token, verify_token
from dotenv import load_dotenv

from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["auth"])


# OAuth setup
oauth = OAuth()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
# The app will still run; note in README to set env vars.
    pass


CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
name='google',
client_id=GOOGLE_CLIENT_ID,
client_secret=GOOGLE_CLIENT_SECRET,
server_metadata_url=CONF_URL,
client_kwargs={'scope': 'openid email profile'},
)


@router.get("/login")
async def login(request: Request, referer: Optional[str] = Header(None)):
    # If called from Swagger UI (/docs), return a dummy 200 response
    if referer and "/docs" in referer:
        return {
            "message": "This endpoint redirects to the Google login page.",
            "action": "In a live website, the user would now be at the Google Auth screen."
        }
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/callback')
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=400, detail="OAuth authorization failed")
    user_info = token.get('userinfo') or await oauth.google.parse_id_token(request, token)
    # user_info contains 'sub' as google unique id
    google_id = user_info.get('sub')
    name = user_info.get('name')
    if not google_id:
        raise HTTPException(status_code=400, detail='No google id returned')


    # check if user exists
    user = db.query(models.Customer).filter(models.Customer.google_id == google_id).first()
    if not user:
        user = models.Customer(name=name or 'No Name', google_id=google_id)
        db.add(user)
        db.commit()
        db.refresh(user)


    access_token = create_access_token(subject=str(user.id))
    # return token to user — in production you'd redirect to frontend with token
    return {"access_token": access_token, "token_type": "bearer"}



# 3️⃣ Verify Token: For Swagger/docs or frontend
@router.get("/verify-token")
async def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user_id = verify_token(token)  # returns UUID string

    user = db.query(models.Customer).filter(models.Customer.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Token is valid", "user_id": str(user.id), "name": user.name}