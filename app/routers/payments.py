from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from .. import models, schemas


router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=schemas.PaymentOut)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # p = models.Payment(status=payment.status, payment_type=payment.payment_type)
    p = models.Payment(
        status=payment.status.value,       # use .value to get string
        payment_type=payment.payment_type.value
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.get("/{transaction_id}", response_model=schemas.PaymentOut)
def get_payment(transaction_id: UUID, db: Session = Depends(get_db)):
    p = db.query(models.Payment).filter(models.Payment.transaction_id == transaction_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")
    return p