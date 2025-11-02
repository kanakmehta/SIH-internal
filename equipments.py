import json
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Equipment
from pathlib import Path

router = APIRouter()

# JSON file path
BASE_DIR = Path(__file__).resolve().parent.parent  # points to 'app/' folder
EQUIPMENTS_JSON_PATH = BASE_DIR / "equipments.json"

print(f"Looking for equipments.json at: {EQUIPMENTS_JSON_PATH}")

# Flag to ensure seeding happens only once
seeded = False

def seed_equipments(session: Session):
    global seeded
    if seeded:
        return  # Already seeded

    # Only seed if table is empty
    if session.exec(select(Equipment)).first():
        seeded = True
        return

    if not EQUIPMENTS_JSON_PATH.exists():
        print(f"⚠️ equipments.json not found at {EQUIPMENTS_JSON_PATH}")
        seeded = True
        return

    with EQUIPMENTS_JSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for eq in data:
        equipment = Equipment(
            id=eq.get("id"),
            owner_id=eq.get("owner_id", 1),
            name=eq.get("name"),
            type=eq.get("type"),
            description=eq.get("description"),
            price_per_day=eq.get("price_per_day"),
            availability=eq.get("availability", True),
            image_url=eq.get("image")
        )
        session.add(equipment)
    session.commit()
    seeded = True
    print(f"✅ Seeded {len(data)} equipments from JSON")


@router.get("/", response_model=list[Equipment])
def get_all_equipments(session: Session = Depends(get_session)):
    seed_equipments(session)
    return session.exec(select(Equipment)).all()


@router.get("/{equipment_id}", response_model=Equipment)
def get_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment
