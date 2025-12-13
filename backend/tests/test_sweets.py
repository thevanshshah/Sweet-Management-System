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

# Helper: Get Normal User Token
def get_user_token(client, username="buyer", password="password123"):
    client.post("/api/auth/register", json={"username": username, "password": password, "role": "customer"})
    response = client.post("/api/auth/login", data={"username": username, "password": password})
    return response.json()["access_token"]

# Helper: Get ADMIN Token
def get_admin_token(client, username="admin", password="admin123"):
    client.post("/api/auth/register", json={"username": username, "password": password, "role": "admin"})
    response = client.post("/api/auth/login", data={"username": username, "password": password})
    return response.json()["access_token"]

def test_read_sweets_empty(client):
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert response.json() == []

def test_create_sweet_as_admin(client):
    """Test that ADMINS can create sweets."""
    token = get_admin_token(client)
    payload = {"name": "Chocolate Fudge", "category": "Fudge", "price": 5.0, "quantity": 100}
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/sweets", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chocolate Fudge"
    assert data["quantity"] == 100

def test_create_sweet_as_customer_fails(client):
    """Test that CUSTOMERS cannot create sweets (403 Forbidden)."""
    token = get_user_token(client)
    payload = {"name": "Hacker Candy", "category": "Fake", "price": 0.0, "quantity": 100}
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/sweets", json=payload, headers=headers)
    
    assert response.status_code == 403 # Should be forbidden

def test_purchase_sweet(client):
    # 1. Admin creates sweet
    admin_token = get_admin_token(client)
    client.post("/api/sweets", json={"name": "Lollipop", "category": "Candy", "price": 0.5, "quantity": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    
    # 2. Customer buys it
    user_token = get_user_token(client)
    sweets = client.get("/api/sweets").json()
    sweet_id = sweets[0]["id"]

    response = client.post(f"/api/sweets/{sweet_id}/purchase", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["quantity"] == 9

def test_restock_sweet(client):
    # 1. Admin creates sweet with 10 items
    admin_token = get_admin_token(client)
    client.post("/api/sweets", json={"name": "Restock Me", "category": "Test", "price": 10, "quantity": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    
    sweets = client.get("/api/sweets").json()
    sweet_id = sweets[0]["id"]

    # 2. Admin Restocks (+10)
    response = client.post(f"/api/sweets/{sweet_id}/restock?amount=10", headers={"Authorization": f"Bearer {admin_token}"})
    
    assert response.status_code == 200
    assert response.json()["quantity"] == 20 # 10 + 10

def test_delete_sweet(client):
    # 1. Create sweet
    admin_token = get_admin_token(client)
    client.post("/api/sweets", json={"name": "Delete Me", "category": "Test", "price": 10, "quantity": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    sweets = client.get("/api/sweets").json()
    sweet_id = sweets[0]["id"]

    # 2. Delete it
    del_response = client.delete(f"/api/sweets/{sweet_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert del_response.status_code == 200

    # 3. Verify it's gone
    get_response = client.get("/api/sweets")
    assert len(get_response.json()) == 0