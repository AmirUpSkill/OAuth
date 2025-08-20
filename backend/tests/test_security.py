from datetime import datetime, timedelta, timezone
import pytest
from jose import jwt, JWTError
from app.core.security import create_access_token
from app.core.config import settings


def test_create_access_token_default_expiration():
    """Test creating an access token with default expiration."""
    test_data = {"sub": "test@example.com", "user_id": "123"}
    
    token = create_access_token(test_data)
    
    # Verify token can be decoded
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode and verify payload
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert payload["user_id"] == "123"
    assert "exp" in payload
    
    # Verify expiration is in the future
    exp_timestamp = payload["exp"]
    current_time = datetime.now(timezone.utc).timestamp()
    assert exp_timestamp > current_time


def test_create_access_token_custom_expiration():
    """Test creating an access token with custom expiration time."""
    test_data = {"sub": "test@example.com"}
    custom_expiration = timedelta(minutes=60)
    
    token = create_access_token(test_data, expires_delta=custom_expiration)
    
    # Decode and verify payload
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    
    # Verify custom expiration time (roughly 1 hour from now)
    exp_timestamp = payload["exp"]
    expected_exp = datetime.now(timezone.utc) + custom_expiration
    
    # Allow 5 seconds tolerance for test execution time
    assert abs(exp_timestamp - expected_exp.timestamp()) < 5


def test_create_access_token_empty_data():
    """Test creating an access token with empty data."""
    token = create_access_token({})
    
    # Should still create a valid token with just expiration
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert "exp" in payload
    assert len(payload) == 1  # Only exp claim


def test_token_expiration():
    """Test that expired tokens are properly rejected."""
    # Create token that expires immediately
    past_time = timedelta(seconds=-1)
    test_data = {"sub": "test@example.com"}
    
    token = create_access_token(test_data, expires_delta=past_time)
    
    # Token should be expired and raise JWTError when decoded
    with pytest.raises(JWTError):
        jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )


def test_token_invalid_signature():
    """Test that tokens with invalid signatures are rejected."""
    test_data = {"sub": "test@example.com"}
    token = create_access_token(test_data)
    
    # Try to decode with wrong secret
    with pytest.raises(JWTError):
        jwt.decode(token, "wrong_secret_key", algorithms=[settings.ALGORITHM])


def test_token_invalid_algorithm():
    """Test that tokens with wrong algorithm are rejected."""
    test_data = {"sub": "test@example.com"}
    token = create_access_token(test_data)
    
    # Try to decode with wrong algorithm
    with pytest.raises(JWTError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
