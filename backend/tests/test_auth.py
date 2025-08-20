import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.users.service import create_user
from app.users.schemas import UserCreate


@pytest.mark.skip(reason="Auth endpoints not implemented yet")
def test_google_login_url(client: TestClient):
    """Test that the Google login URL endpoint returns a valid authorization URL."""
    response = client.get("/api/v1/auth/login/google")
    
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    
    # Verify the URL contains expected Google OAuth parameters
    auth_url = data["authorization_url"]
    assert "accounts.google.com/o/oauth2/v2/auth" in auth_url
    assert "response_type=code" in auth_url
    assert "client_id=" in auth_url
    assert "redirect_uri=" in auth_url
    assert "scope=" in auth_url
    assert "state=" in auth_url


@pytest.mark.skip(reason="Auth service functions not implemented yet")
def test_google_login_url_error_handling(client: TestClient):
    """Test error handling when Google login URL generation fails."""
    with patch('app.auth.service.generate_google_auth_url') as mock_generate:
        mock_generate.side_effect = Exception("OAuth service unavailable")
        
        response = client.get("/api/v1/auth/login/google")
        
        assert response.status_code == 500
        assert "detail" in response.json()


@pytest.mark.skip(reason="Auth callback endpoint not implemented yet")
@patch('app.auth.service.exchange_code_for_tokens')
@patch('app.auth.service.get_google_user_info')
def test_google_callback_success_new_user(
    mock_get_user_info: MagicMock,
    mock_exchange_tokens: MagicMock,
    client: TestClient,
    db_session: Session
):
    """Test successful Google OAuth callback with new user registration."""
    # Mock the OAuth flow responses
    mock_exchange_tokens.return_value = {
        "access_token": "mock_access_token",
        "id_token": "mock_id_token"
    }
    
    mock_get_user_info.return_value = {
        "email": "newuser@gmail.com",
        "name": "New User",
        "picture": "https://example.com/avatar.jpg"
    }
    
    # Call the callback endpoint
    response = client.get(
        "/api/v1/auth/callback/google",
        params={"code": "mock_auth_code", "state": "mock_state"},
        follow_redirects=False  # Don't follow the redirect for testing
    )
    
    # Should redirect to frontend
    assert response.status_code == 307
    assert "Location" in response.headers
    
    # Should set the access token cookie
    assert "Set-Cookie" in response.headers
    cookie_header = response.headers["Set-Cookie"]
    assert "access_token=" in cookie_header
    assert "HttpOnly" in cookie_header
    assert "SameSite" in cookie_header


@pytest.mark.skip(reason="Auth callback endpoint not implemented yet")
@patch('app.auth.service.exchange_code_for_tokens')
@patch('app.auth.service.get_google_user_info')
def test_google_callback_success_existing_user(
    mock_get_user_info: MagicMock,
    mock_exchange_tokens: MagicMock,
    client: TestClient,
    db_session: Session
):
    """Test successful Google OAuth callback with existing user login."""
    # Create an existing user
    existing_user = create_user(
        db_session, 
        UserCreate(email="existing@gmail.com", full_name="Existing User")
    )
    
    # Mock the OAuth flow responses
    mock_exchange_tokens.return_value = {
        "access_token": "mock_access_token",
        "id_token": "mock_id_token"
    }
    
    mock_get_user_info.return_value = {
        "email": "existing@gmail.com",
        "name": "Existing User Updated",
        "picture": "https://example.com/new_avatar.jpg"
    }
    
    # Call the callback endpoint
    response = client.get(
        "/api/v1/auth/callback/google",
        params={"code": "mock_auth_code", "state": "mock_state"},
        follow_redirects=False
    )
    
    # Should redirect successfully
    assert response.status_code == 307
    assert "Set-Cookie" in response.headers


@pytest.mark.skip(reason="Auth callback endpoint not implemented yet")
def test_google_callback_missing_code(client: TestClient):
    """Test Google callback with missing authorization code."""
    response = client.get(
        "/api/v1/auth/callback/google",
        params={"state": "mock_state"},  # Missing 'code' parameter
        follow_redirects=False
    )
    
    # Should redirect to error page
    assert response.status_code == 307
    assert "error=" in response.headers.get("Location", "")


@pytest.mark.skip(reason="Auth callback endpoint not implemented yet")
def test_google_callback_missing_state(client: TestClient):
    """Test Google callback with missing state parameter."""
    response = client.get(
        "/api/v1/auth/callback/google",
        params={"code": "mock_code"},  # Missing 'state' parameter
        follow_redirects=False
    )
    
    # Should redirect to error page
    assert response.status_code == 307
    assert "error=" in response.headers.get("Location", "")


@pytest.mark.skip(reason="Auth callback endpoint not implemented yet")
@patch('app.auth.service.exchange_code_for_tokens')
def test_google_callback_oauth_error(
    mock_exchange_tokens: MagicMock,
    client: TestClient
):
    """Test Google callback when OAuth exchange fails."""
    # Mock OAuth failure
    mock_exchange_tokens.side_effect = Exception("OAuth exchange failed")
    
    response = client.get(
        "/api/v1/auth/callback/google",
        params={"code": "invalid_code", "state": "mock_state"},
        follow_redirects=False
    )
    
    # Should redirect to error page
    assert response.status_code == 307
    assert "error=" in response.headers.get("Location", "")


@pytest.mark.skip(reason="Auth logout endpoint not implemented yet")
def test_logout_success(client: TestClient, db_session: Session):
    """Test successful logout."""
    # Create a user and get a token
    user = create_user(db_session, UserCreate(email="logout@example.com", full_name="Logout User"))
    
    # Set a cookie first (simulate logged in state)
    client.cookies.set("access_token", "some_jwt_token")
    
    # Call logout endpoint
    response = client.post("/api/v1/auth/logout")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Should clear the access token cookie
    assert "Set-Cookie" in response.headers
    cookie_header = response.headers["Set-Cookie"]
    assert "access_token=;" in cookie_header  # Empty value means cleared
    assert "Max-Age=0" in cookie_header


@pytest.mark.skip(reason="Auth logout endpoint not implemented yet")
def test_logout_without_cookie(client: TestClient):
    """Test logout when no authentication cookie is present."""
    response = client.post("/api/v1/auth/logout")
    
    # Should still return success (idempotent operation)
    assert response.status_code == 200
