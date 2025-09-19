from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from datetime import datetime, timedelta
from ..database import get_db
from .. import models, schemas
from ..utils import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter(prefix="/orders", tags=["orders"])

# ------------------- Create Order -------------------
@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order_in: schemas.OrderCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user_id = verify_token(token)

    payment = db.query(models.Payment).filter(models.Payment.transaction_id == order_in.transaction_id).first()
    if not payment:
        raise HTTPException(status_code=400, detail="Payment not found")
    if payment.status != models.PaymentStatusEnum.pass_status:
        raise HTTPException(status_code=400, detail="Payment not successful")

    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == order_in.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=400, detail="Restaurant not found")

    order = models.Order(
        food_item=order_in.food_item,
        transaction_id=order_in.transaction_id,
        restaurant_id=order_in.restaurant_id,
        customer_id=user_id
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# Add this function to the BOTTOM of your orders.py file

@router.get("/debug/test_order_type")
def debug_order_type(db: Session = Depends(get_db)):
    """
    A temporary endpoint to debug the data type of the food_item column.
    """
    print("--- RUNNING DEBUG TEST ---")
    
    # Try to get the very first order from the database
    first_order = db.query(models.Order).first()
    
    if not first_order:
        print("DEBUG: No orders found in the database.")
        raise HTTPException(status_code=404, detail="No orders found to test.")
        
    food_item_value = first_order.food_item
    food_item_type = type(food_item_value)
    
    # This print statement is the most important part.
    # We will check its output in your terminal.
    print(f"DEBUG: Fetched food item: '{food_item_value}'")
    print(f"DEBUG: The Python type is: {food_item_type}")
    print("--------------------------")
    
    return {
        "message": "Debug test complete. Check your terminal logs for the Python type.",
        "food_item_value": str(food_item_value),
        "python_type": str(food_item_type)
    }

# ------------------- Helper: price mapping -------------------
price_map = {
    'veg_manchurian': 150,
    'chicken_manchurian': 200,
    'veg_fried_rice': 120,
    'chicken_noodles': 180,
}

# ------------------- Report 1: Total earnings in Mumbai last month -------------------
@router.get('/reports/mumbai/last_month')
def earnings_mumbai_last_month(db: Session = Depends(get_db)):
    today = datetime.utcnow()
    first_day_this_month = today.replace(day=1)
    last_month_end = first_day_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # Create the case statement using the enum values
    whens = {models.Order.food_item == value: price for value, price in price_map.items()}
    case_stmt = case(*[(condition, value) for condition, value in whens.items()], else_=0)

    total = (
        db.query(func.sum(case_stmt))
        .join(models.Restaurant, models.Order.restaurant_id == models.Restaurant.restaurant_id)
        .join(models.Payment, models.Order.transaction_id == models.Payment.transaction_id)
        .filter(models.Restaurant.area == models.AreaEnum.Mumbai)
        .filter(models.Payment.status == models.PaymentStatusEnum.pass_status)
        .filter(models.Order.created_at >= last_month_start)
        .filter(models.Order.created_at <= last_month_end)
        .scalar()
    )

    return {"total_earnings_mumbai_last_month": float(total or 0)}

# ------------------- Report 2: Veg earnings in Bangalore -------------------
@router.get('/reports/bangalore/veg_earnings')
def veg_earnings_bangalore(db: Session = Depends(get_db)):
    veg_map = {
        'veg_manchurian': 150,
        'veg_fried_rice': 120,
    }

    # Create the case statement using the enum values
    whens = {models.Order.food_item == value: price for value, price in veg_map.items()}
    case_stmt = case(*[(condition, value) for condition, value in whens.items()], else_=0)

    total = (
        db.query(func.sum(case_stmt))
        .join(models.Restaurant, models.Order.restaurant_id == models.Restaurant.restaurant_id)
        .join(models.Payment, models.Order.transaction_id == models.Payment.transaction_id)
        .filter(models.Restaurant.area == models.AreaEnum.Bangalore)
        .filter(models.Payment.status == models.PaymentStatusEnum.pass_status)
        .scalar()
    )

    return {"veg_earnings_bangalore": float(total or 0)}

# ------------------- Report 3: Top 3 customers -------------------
@router.get('/reports/top_customers')
def top_customers(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Customer.name, func.count(models.Order.order_id).label("orders_count"))
        .join(models.Order, models.Customer.id == models.Order.customer_id)
        .group_by(models.Customer.name)
        .order_by(func.count(models.Order.order_id).desc())
        .limit(3)
        .all()
    )
    return [{"name": r[0], "orders_count": r[1]} for r in rows]

# ------------------- Report 4: Daily revenue past 7 days (CORRECTED) -------------------
@router.get('/reports/daily_revenue_7days')
def daily_revenue_7days(db: Session = Depends(get_db)):
    case_stmt = case(price_map, value=models.Order.food_item, else_=0)
    
    # Define the labeled column as a variable
    day_column = func.date_trunc("day", models.Order.created_at).label("day")

    rows = (
        db.query(
            day_column,
            models.Restaurant.area,
            func.sum(case_stmt).label("revenue")
        )
        .join(models.Restaurant, models.Order.restaurant_id == models.Restaurant.restaurant_id)
        .join(models.Payment, models.Order.transaction_id == models.Payment.transaction_id)
        .filter(models.Payment.status == models.PaymentStatusEnum.pass_status)
        .filter(models.Order.created_at >= datetime.utcnow() - timedelta(days=7))
        # Use the variable in group_by and order_by
        .group_by(day_column, models.Restaurant.area)
        .order_by(day_column.desc())
        .all()
    )

    return [{"date": r[0].date(), "area": r[1].value, "revenue": float(r[2] or 0)} for r in rows]

# ------------------- Report 5: Orders summary for specific restaurant -------------------
@router.get('/reports/restaurant/{restaurant_id}/summary')
def restaurant_summary(restaurant_id: str, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Order.food_item, func.count(models.Order.order_id))
        .join(models.Payment, models.Order.transaction_id == models.Payment.transaction_id)
        .filter(models.Order.restaurant_id == restaurant_id)
        .filter(models.Payment.status == models.PaymentStatusEnum.pass_status)
        .group_by(models.Order.food_item)
        .all()
    )

    return [{"food_item": r[0].value, "count": r[1]} for r in rows]