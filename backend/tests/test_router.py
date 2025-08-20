import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.users.service import create_user
from app.users.schemas import UserCreate


@pytest.mark.skip(reason="User /me endpoint not implemented yet")
def test_get_me_success(client: TestClient, db_session: Session):
    """Test successful retrieval of current user info."""
    # Create a test user
    user = create_user(db_session, UserCreate(email="me@example.com", full_name="Test User"))
    
    # Create a valid JWT token with user ID
    token = create_access_token({"sub": str(user.id), "email": user.email})
    
    # Call the /me endpoint with valid token
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verify successful response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Test User"
    assert data["id"] == str(user.id)


@pytest.mark.skip(reason="User /me endpoint not implemented yet")
def test_get_me_unauthorized_no_token(client: TestClient):
    """Test that accessing /me without token returns 401."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.skip(reason="User /me endpoint not implemented yet")
def test_get_me_unauthorized_invalid_token(client: TestClient):
    """Test that accessing /me with invalid token returns 401."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.skip(reason="User /me endpoint not implemented yet")
def test_get_me_user_not_found(client: TestClient):
    """Test that accessing /me with valid token but non-existent user returns 404."""
    # Create token with fake user ID
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    token = create_access_token({"sub": fake_user_id, "email": "fake@example.com"})
    
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
