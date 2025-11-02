from fastapi import FastAPI
from app.routers import auth, equipments, bookings
from app.database import create_db_and_tables, get_db
from sqlalchemy.orm import Session
from app.models import Equipment
import os
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel



app = FastAPI(title="Farm Rent Backend")

class User(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("kisaan.sql")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (user.email, user.password))
    result = cur.fetchone()
    conn.close()
    
    if result:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/")
def root():
    return RedirectResponse(url="/login-page")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Create database and tables
    create_db_and_tables()

    # Absolute path to equipments.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "equipments.json")

    # Load equipments into database
    try:
        db: Session = next(get_db())
        with open(file_path, "r") as f:
            equipments_data = json.load(f)
        
        for eq in equipments_data:
            # Check if equipment already exists
            existing = db.query(Equipment).filter(Equipment.id == eq["id"]).first()
            if not existing:
                new_eq = Equipment(
                    id=eq["id"],
                    name=eq["name"],
                    type=eq["type"],
                    description=eq.get("description", "No description provided"),
                    price_per_day=eq.get("price_per_day", 0),  # Required!
                    availability=eq.get("availability", True),
                    owner_id=eq.get("owner_id", 1),           # Required!
                    image_url=eq.get("image") or "https://via.placeholder.com/400x300"
                )
                db.add(new_eq)
        db.commit()
        print("✅ Equipments dataset loaded successfully")
    except Exception as e:
        print(f"⚠️ Failed to load equipments dataset: {e}")

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(equipments.router, prefix="/equipments", tags=["equipments"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

@app.get("/")
def read_root():
    return {"message": "Farm Rent Backend is running 🚜"}



