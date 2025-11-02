from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file!")

engine = create_engine(DATABASE_URL, echo=True)

# Create all tables at startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ✅ Dependency for FastAPI
def get_db():
    with Session(engine) as session:
        yield session

# Optional: keep the original name for clarity
get_session = get_db
