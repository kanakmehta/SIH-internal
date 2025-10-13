import os
import json
from app.database import engine
from sqlmodel import Session, SQLModel, select
from app.models import Equipment

# Create tables if they don’t exist
SQLModel.metadata.create_all(engine)

# Get absolute path to equipments.json (inside app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # project root
file_path = os.path.join(BASE_DIR, "app", "equipments.json")

print("Looking for JSON at:", file_path)  # Debugging

# Load equipments from JSON file
with open(file_path, "r") as f:
    equipments_data = json.load(f)

# Convert JSON objects into Equipment model instances
equipments = [
    Equipment(
        id=eq.get("id"),
        name=eq.get("name"),
        type=eq.get("type"),
        description=eq.get("description"),
        price_per_day=eq.get("price_per_day"),
        availability=eq.get("availability", True),
        owner_id=eq.get("owner_id", 1),
        image_url=eq.get("image")  # ✅ map JSON "image" to DB "image_url"
    )
    for eq in equipments_data
]


with Session(engine) as session:
    # Prevent duplicates
    existing = session.exec(select(Equipment)).all()
    if not existing:
        session.add_all(equipments)
        session.commit()
        print("✅ Seeded equipments successfully from JSON!")
    else:
        print("⚡ Equipments already exist, skipping seeding.")

