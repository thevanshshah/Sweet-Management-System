import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

# --- PATH FIX ---
# This ensures we can import from the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# ----------------

from main import app, engine
from models import Sweet

@pytest.fixture(name="client")
def client_fixture():
    """
    Create a TestClient that triggers startup/shutdown events.
    This ensures create_db_and_tables() runs before tests.
    """
    # clear the tables before tests to ensure a clean slate
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    with TestClient(app) as client:
        yield client

def test_read_sweets_empty(client):
    """
    Test that the /api/sweets endpoint returns an empty list initially.
    """
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert response.json() == []

def test_create_sweet(client):
    """
    Test that we can create a new sweet via POST /api/sweets.
    """
    payload = {
        "name": "Chocolate Fudge",
        "category": "Fudge",
        "price": 5.0,
        "quantity": 100
    }
    
    response = client.post("/api/sweets", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chocolate Fudge"
    assert data["quantity"] == 100
    assert "id" in data