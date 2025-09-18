from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class AreaEnum(str, Enum):
	Mumbai = "Mumbai"
	Bangalore = "Bangalore"


class PaymentStatusEnum(str, Enum):
    pass_status = "pass"
    fail = "fail"


class PaymentTypeEnum(str, Enum):
    UPI = "UPI"
    card = "card"


class FoodItemEnum(str, Enum):
    veg_manchurian = "veg_manchurian"
    chicken_manchurian = "chicken_manchurian"
    veg_fried_rice = "veg_fried_rice"
    chicken_noodles = "chicken_noodles"


class CustomerIn(BaseModel):
    name: str
    google_id: str
    age: Optional[int]


class CustomerOut(CustomerIn):
    id: UUID


class PaymentCreate(BaseModel):
    payment_type: PaymentTypeEnum
    status: PaymentStatusEnum


class PaymentOut(BaseModel):
    transaction_id: UUID
    status: PaymentStatusEnum
    payment_type: PaymentTypeEnum
    created_at: datetime


class OrderCreate(BaseModel):
    food_item: FoodItemEnum
    transaction_id: UUID
    restaurant_id: UUID


class OrderOut(BaseModel):
    order_id: UUID
    food_item: FoodItemEnum
    transaction_id: UUID
    restaurant_id: UUID
    customer_id: UUID
    created_at: datetime


class RestaurantIn(BaseModel):
    restaurant_name: str
    area: AreaEnum


class RestaurantOut(RestaurantIn):
    restaurant_id: UUID