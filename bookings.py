
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.database import get_session
from app.routers.auth import get_current_user
router = APIRouter()

@router.post("/bookings")
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    equipment = db.get(models.Equipment, booking.equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    try:
        start_date = datetime.strptime(booking.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(booking.end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if end_date <= start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    rental_days = (end_date - start_date).days
    total_amount = rental_days * equipment.price_per_day

    db_booking = models.Booking(
        equipment_id=booking.equipment_id,
        renter_id=current_user.id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        total_amount=total_amount,
        status="pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking
