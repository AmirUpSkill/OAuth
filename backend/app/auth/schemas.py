from pydantic import BaseModel, HttpUrl
from typing import Optional

# --- Schema Layer ---
class AuthURL(BaseModel):
    """
    Schema for the response that provides the Google OAuth 
    authorization URL.
    """
    authorization_url: HttpUrl

class LoginResponse(BaseModel):
    """
    Schema for successful login response.
    """
    message: str
    user_id: str

class TokenValidationResponse(BaseModel):
    """
    Schema for token validation response.
    """
    valid: bool
    user_id: Optional[str] = None
    expires_at: Optional[int] = None

class LogoutResponse(BaseModel):
    """
    Schema for logout response.
    """
    message: str

