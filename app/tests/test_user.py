from app import models
from datetime import datetime


def test_create_user(client):
    payload = {
        "email": "testuser@example.com",
        "password": "securepass"
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

def test_get_user(client, session):
    user = models.User(
        email="testuser@example.com",
        password="hashedpassword",
        created_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.get(f"/users/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email
