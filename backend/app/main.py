import os
import time
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
import sqlite3

# --- Configuration (using Pydantic BaseSettings) ---
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")  # You MUST change this
    database_url: str = Field(default="sqlite:///./thinkalike.db", env="DATABASE_URL") # SQLite for dev
    # Add other settings here as needed (e.g., API keys, model paths)

    class Config:
        env_file = ".env"  # Load environment variables from a .env file

settings = Settings()

# --- FastAPI Setup ---
app = FastAPI(
    title="ThinkAlike API",
    version="0.1.0",
    description="API for the ThinkAlike platform.",
)

# --- CORS Configuration ---
# IMPORTANT: For production, be more restrictive!
origins = [
    "http://localhost:3000",   # Allow your React development server
    "https://thinkalike-project.onrender.com",  # Your *deployed* documentation site
    "*" #remove this on production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods for development
    allow_headers=["*"],  # Allow all headers for development
)

# --- Pydantic Models (Data Structures) ---
# These define the structure of your data and are used for validation and documentation
class User(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str | None = None  # Optional field
    profile_picture_url: str | None = None
    created_at: str
    is_active: bool
    bio: str | None = None
    # Add other relevant fields as needed

    class Config:
        orm_mode = True # To work directly with SQLAlchemy

class Profile(BaseModel): #You can add more fields as necessary
    profile_id: int
    user_id: int
    bio: str
    birthdate: str
    location: str | None = None
    profile_picture_url: str | None = None

class Connection(BaseModel):
    connection_id: int
    user1_id: int
    user2_id: int
    status: str
    created_at: str

class ValueInterest(BaseModel): #Simplified example. You might need more tables
    value_interest_id: int
    user_id: int
    category: str
    value: str
    importance: int

class ConnectionStatus(BaseModel): #Example of a simple request body model
    status: str

# --- Database Interaction (using SQLite for now) ---
DATABASE_FILE = "thinkalike.db"

def get_db(): #Database connection
    db = None
    try:
        db = sqlite3.connect(settings.database_url.replace("sqlite:///", "")) #Adapt the path
        db.row_factory = sqlite3.Row  # Use Row factory to get dictionary-like results
        yield db
    finally:
        if db:
            db.close()

# --- API Endpoints ---
@app.get("/api/v1/graph")
async def get_graph_data(db: sqlite3.Connection = Depends(get_db)):
    # For now, return some static data.  Later, you'll fetch this from a database.
    # This is just a *minimal* example to get you started.  You'll replace this
    # with actual database queries.
    cursor = db.cursor()
    try:
      cursor.execute("SELECT * FROM Users")
      users = cursor.fetchall()
      print(users) # So you can check that your database is working
    except:
      return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error loading users table."})

    data = {
      "nodes": [
        { "id": 'node1', "label": 'User Input', "group": 1 , "value": "User data input"},
        { "id": 'node2', "label": 'AI Agent', "group": 4, "isAI": True, "value": "AI processing node" },
        { "id": 'node3', "label": 'Database', "group": 3, "value": "Persistent data storage" },
        { "id": 'node4', "label": 'Response', "group": 2, "value": "Response to the user" }
      ],
      "edges": [
        { "from": 'node1', "to": 'node2', "value": "User data" },
        { "from": 'node2', "to": 'node3', "value": "AI processed data" },
        { "from": 'node3', "to": 'node4', "value": "Data for response" },
      ]
    }
    return data

# TEMPORARY endpoint to simulate connection status changes
@app.post("/api/v1/connection/status")
async def set_connection_status(status: ConnectionStatus):
    # In a real application, this would update the database
    # For now, we just return the status for testing purposes.
    if status.status not in ["disconnected", "connecting", "connected"]:
        raise HTTPException(status_code=400, detail="Invalid status")  # Use HTTPException
    return {"status": status.status}

# Placeholder endpoint for user registration
@app.post("/api/v1/users", response_model=User) # Use the Pydantic model!
async def create_user(user: User):
  #TODO
  return user

# Placeholder endpoint for user login
@app.post("/api/v1/auth/login")
async def login_user():
    # Placeholder - Implement JWT authentication here
    return {"message": "Login (to be implemented)"}

# Example of a protected endpoint (requires authentication)
@app.get("/api/v1/users/{user_id}", response_model=User)
async def get_user(user_id: int):
  # Placeholder. In a real app, verify JWT and fetch user from DB
    user = User(
        user_id=user_id,
        username=f"user{user_id}",  # Replace with data from your database
        email="test@example.com",
        created_at="2024-02-29T12:00:00Z",
        is_active=True,
    )
    return user
