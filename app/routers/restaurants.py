from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post('/', response_model=schemas.RestaurantOut)
def create_restaurant(r: schemas.RestaurantIn, db: Session =
    Depends(get_db)):
    rest = models.Restaurant(restaurant_name=r.restaurant_name, area=r.area)
    db.add(rest)
    db.commit()
    db.refresh(rest)
    return rest

@router.get('/{restaurant_id}', response_model=schemas.RestaurantOut)
def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    rest = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id
    == restaurant_id).first()
    if not rest:
        raise HTTPException(404, "Restaurant not found")
    return rest