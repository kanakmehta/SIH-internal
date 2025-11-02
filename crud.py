from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Path to frontend directory (one level up)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# ✅ Serve static frontend
app.mount("/static", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ✅ Default route -> dashboard.html
@app.get("/")
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JSON file to store users
DB_FILE = "users.json"

# Load users from JSON file at startup
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        try:
            users_db = json.load(f)
        except json.JSONDecodeError:
            users_db = {}
else:
    users_db = {}

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Helper to save users to JSON
def save_users():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f)

# Signup endpoint
@app.post("/users/signup")
def signup(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = pwd_context.hash(user.password)
    users_db[user.username] = {"username": user.username, "password": hashed}
    save_users()
    return {"message": "User created successfully"}

# Login endpoint
@app.post("/users/login")
def login(user: UserLogin):
    db_user = users_db.get(user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # For simplicity, just return username as token (demo)
    return {"token": user.username, "username": user.username}
