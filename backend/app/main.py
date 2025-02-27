import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings, Field, BaseModel

from backend.app.endpoints import agent_routes, feedback_routes
from .config import settings  # Use settings defined in config.py

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

# Accessing configuration settings for testing/demonstration
if settings.debug:
    print(f"Debug mode: {settings.debug}")
print(f"Database URL: {settings.database_url}")

# VERY BASIC EXAMPLE ENDPOINT (replace with your actual data)
@app.get("/api/v1/graph")
async def get_graph_data():
    """
    Retrieve graph data.

    This endpoint returns static graph data for demonstration purposes.
    In a real application, this data would be fetched from a database.

    Returns:
        dict: A dictionary containing nodes and edges of the graph.
    """
    return {"nodes": [], "edges": []}

class ConnectionStatus(BaseModel):
    status: str

# TEMPORARY endpoint to simulate connection status changes
@app.post("/api/v1/connection/status")
async def set_connection_status(status: ConnectionStatus):
    """
    Asynchronously sets the connection status.

    Args:
        status (ConnectionStatus): An instance of ConnectionStatus containing the status to be set.

    Returns:
        dict: A dictionary containing the status for testing purposes.
    """
    if status.status not in ["disconnected", "connecting", "connected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    return {"status": status.status}
