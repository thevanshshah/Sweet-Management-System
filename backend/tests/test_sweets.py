import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

# --- PATH FIX ---
# This ensures we can import from the parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# ----------------

from main import app, engine

@pytest.fixture(name="client")
def client_fixture():
    """
    Create a TestClient that triggers startup/shutdown events.
    This ensures create_db_and_tables() runs before tests.
    """
    # Clear the tables before tests to ensure a clean slate
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    with TestClient(app) as client:
        yield client

# Helper function to get an auth token
def get_auth_token(client, username="buyer", password="password123"):
    # 1. Register
    client.post("/api/auth/register", json={"username": username, "password": password})
    # 2. Login
    response = client.post("/api/auth/login", data={"username": username, "password": password})
    return response.json()["access_token"]

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

def test_purchase_sweet(client):
    """
    Test purchasing a sweet decreases its quantity.
    *Requires Authentication*
    """
    # 1. Create a sweet with 10 items
    payload = {"name": "Lollipop", "category": "Hard Candy", "price": 0.5, "quantity": 10}
    create_res = client.post("/api/sweets", json=payload)
    sweet_id = create_res.json()["id"]

    # 2. Get Token (Register & Login)
    token = get_auth_token(client)

    # 3. Purchase one item WITH Authorization header
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/api/sweets/{sweet_id}/purchase", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 9  # Should drop from 10 to 9

def test_purchase_out_of_stock(client):
    """
    Test that purchasing fails if quantity is 0.
    *Requires Authentication*
    """
    # 1. Create a sweet with 0 items
    payload = {"name": "Rare Candy", "category": "Special", "price": 100.0, "quantity": 0}
    create_res = client.post("/api/sweets", json=payload)
    sweet_id = create_res.json()["id"]

    # 2. Get Token
    token = get_auth_token(client)

    # 3. Try to purchase WITH Token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(f"/api/sweets/{sweet_id}/purchase", headers=headers)
    
    # Should fail with 400 Bad Request
    assert response.status_code == 400
    assert response.json()["detail"] == "Sweet out of stock"

def test_purchase_unauthorized(client):
    """
    Test that purchasing FAILS if the user is not logged in.
    """
    # 1. Create a sweet
    payload = {"name": "Forbidden Candy", "category": "Special", "price": 10.0, "quantity": 5}
    create_res = client.post("/api/sweets", json=payload)
    sweet_id = create_res.json()["id"]

    # 2. Try to purchase WITHOUT Token
    response = client.post(f"/api/sweets/{sweet_id}/purchase")
    
    # Should fail with 401 Unauthorized
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"