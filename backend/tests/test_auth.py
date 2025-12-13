import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

# --- PATH FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# ----------------

from main import app, engine

@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client

def test_register_user(client):
    """
    Test that a new user can register successfully.
    """
    payload = {
        "username": "candy_fan",
        "password": "securepassword123"
    }
    
    response = client.post("/api/auth/register", json=payload)
    
    assert response.status_code == 201  # 201 Created
    data = response.json()
    assert data["username"] == "candy_fan"
    assert "password" not in data  # NEVER return the password!
    assert "id" in data