from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, payments, orders, restaurants
import os
from starlette.middleware.sessions import SessionMiddleware
# create tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Food Ordering Backend with Google OAuth")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "random_secret_key"))
app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(orders.router)
app.include_router(restaurants.router)

@app.get('/')
def root():
    return {"message": "FastAPI Food Ordering Backend"}