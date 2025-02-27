import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import agent_routes, feedback_routes
# Correct relative import for your project structure:
from backend.routes import agent_routes, feedback_routes
from pydantic_settings import BaseSettings, Field

class Settings(BaseSettings):
    debug: bool = Field(default=False)
    database_url: str = Field(...)

settings = Settings()

app = FastAPI(
    title="ThinkAlike"
)

# CORS (Cross-Origin Resource Sharing) configuration - ALLOW ALL origins for now
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Start with allowing all origins, restrict later
    allow_credentials=True,
    allow_methods=["*"],    # Allow all methods
    allow_headers=["*"],    # Allow all headers
)

# Include your API routers
app.include_router(agent_routes.router)
app.include_router(feedback_routes.router)

# Accessing configuration settings (for testing/demonstration - you can remove these later)
print(f"Debug mode: {settings.debug}")
print(f"Database URL: {settings.database_url}")

# VERY BASIC EXAMPLE ENDPOINT (replace with your actual data)
@app.get("/api/v1/graph")
async def get_graph_data():
    # For now, return some static data. Later, you'll fetch this from a database.
    data = {
        "nodes": [
            {"id": 'node1', "label": 'User Input', "group": 1, "value": "User data input"},
            {"id": 'node2', "label": 'AI Agent', "group": 4, "isAI": True, "value": "AI processing node"},
            {"id": 'node3', "label": 'Database', "group": 3, "value": "Persistent data storage"},
            {"id": 'node4', "label": 'Response', "group": 2, "value": "Response to the user"}
        ],
        "edges": [
            {"from": 'node1', "to": 'node2', "value": "User data"},
            {"from": 'node2', "to": 'node3', "value": "AI processed data"},
            {"from": 'node3', "to": 'node4', "value": "Data for response"},
        ]
    }
    return data

# TEMPORARY endpoint to simulate connection status changes
@app.post("/api/v1/connection/status")
async def set_connection_status(status: str):  # You'll likely want a Pydantic model here
    # In a real application, this would update the database
    # For now, we just return the status for testing purposes.
    if status not in ["disconnected", "connecting", "connected"]:
        return {"error": "Invalid status"}  # Basic validation
    return {"status": status}
