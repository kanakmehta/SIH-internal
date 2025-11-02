from typing import Optional
from pydantic import BaseModel

# -------- USERS --------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True   # 👈 lets FastAPI read from SQLAlchemy/SQLModel objects


# -------- EQUIPMENTS --------
class EquipmentCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    price_per_day: float
    image_url: Optional[str] = None


class EquipmentRead(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    price_per_day: float
    image_url: Optional[str] = None
    availability: bool

    class Config:
        orm_mode = True   # 👈 required when returning DB models directly


# -------- BOOKINGS --------
class BookingCreate(BaseModel):
    equipment_id: int
    start_date: str   # 👈 might want to change these to datetime.date
    end_date: str
    total_amount: float


class BookingRead(BaseModel):
    id: int
    equipment_id: int
    renter_id: int
    start_date: str   # same here, maybe datetime.date
    end_date: str
    total_amount: float
    status: str

    class Config:
        orm_mode = True
