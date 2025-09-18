import enum
import uuid
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base


class AreaEnum(enum.Enum):
    Mumbai = "Mumbai"
    Bangalore = "Bangalore"


class PaymentStatusEnum(str, enum.Enum):
    pass_status = "pass"
    fail = "fail"


class PaymentTypeEnum(str, enum.Enum):
    UPI = "UPI"
    card = "card"


class FoodItemEnum(enum.Enum):
    veg_manchurian = "veg_manchurian"
    chicken_manchurian = "chicken_manchurian"
    veg_fried_rice = "veg_fried_rice"
    chicken_noodles = "chicken_noodles"


class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer)
    orders = relationship("Order", back_populates="customer")


class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_name = Column(String, nullable=False)
    area = Column(Enum(AreaEnum), nullable=False, index=True)
    orders = relationship("Order", back_populates="restaurant")


class Payment(Base):
    __tablename__ = "payments"
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(PaymentStatusEnum), nullable=False, index=True)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    order = relationship("Order", back_populates="payment", uselist=False)


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_item = Column(Enum(FoodItemEnum, native_enum=True), nullable=False)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("payments.transaction_id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.restaurant_id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    payment = relationship("Payment", back_populates="order")
    restaurant = relationship("Restaurant", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")