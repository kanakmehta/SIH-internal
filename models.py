from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    role: str  # 'owner' or 'renter'

    # Relationship: One user can own multiple equipments
    equipments: List["Equipment"] = Relationship(back_populates="owner")
    bookings: List["Booking"] = Relationship(back_populates="renter")


class Equipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    type: str
    description: Optional[str] = None
    price_per_day: float
    availability: bool = True
    image_url: Optional[str] = None

    # Relationships
    owner: Optional[User] = Relationship(back_populates="equipments")
    bookings: List["Booking"] = Relationship(back_populates="equipment")


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    equipment_id: int = Field(foreign_key="equipment.id")
    renter_id: int = Field(foreign_key="user.id")
    start_date: str
    end_date: str
    total_amount: float
    status: str = Field(default="requested")  # requested / confirmed / completed / cancelled

    # Relationships
    equipment: Optional[Equipment] = Relationship(back_populates="bookings")
    renter: Optional[User] = Relationship(back_populates="bookings")
