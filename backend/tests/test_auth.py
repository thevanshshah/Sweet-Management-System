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

def test_login_and_get_token(client):
    """
    Test that a registered user can login and get a JWT token.
    """
    # 1. Register a user
    client.post("/api/auth/register", json={"username": "token_user", "password": "password123"})
    
    # 2. Login
    login_data = {
        "username": "token_user",
        "password": "password123"
    }
    # Note: OAuth2PasswordRequestForm usually expects form data, not JSON, 
    # but for simplicity in this specific endpoint, we'll verify what our implementation requires.
    # Standard FastAPI OAuth2 implementation uses form-data.
    response = client.post("/api/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"