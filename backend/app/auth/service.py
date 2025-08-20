from typing import Dict
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import HTTPException
from app.core.config import settings
from app.db.models import User
from app.users.service import get_user_by_email, create_user
from app.users.schemas import UserCreate
from app.core.security import create_access_token

# --- Initialize OAuth  Client --- 
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    }
)
# --- Method to get the google auth url --- 
def get_google_authorization_url(redirect_uri: str) -> str:
    """
    Generates the Google OAuth authorization URL.
    """
    google_client = oauth.create_client('google')
    if not google_client:
        raise HTTPException(status_code=500, detail="Google OAuth client not configured")
    
    authorization_url, state = google_client.create_authorization_url(
        "https://accounts.google.com/o/oauth2/v2/auth",
        redirect_uri=redirect_uri
    )
    return authorization_url

# ---- Method to handle_google_callback ----
async def handle_google_callback(request , db: Session ) -> User : 
    """
        Handles the Google OAuth Callback : 
        1. Exchanges code for access token 
        2. Fetches user info 
        3. Creates or retrieves user in DB 
        4. Returns the user object 
    """
    try:
        google_client = oauth.create_client('google')
        if not google_client:
            raise HTTPException(status_code=500, detail="Google OAuth client not configured")
            
        token = await google_client.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
        email = user_info.get("email")
        full_name = user_info.get("name")
        user = get_user_by_email(db, email)
        if not user:
            user = create_user(db, UserCreate(email=email, full_name=full_name))
        return user
    except OAuthError as oauth_error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(oauth_error)}")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to handle Google callback: {str(exc)}")
    
def create_user_token(user: User) -> str:
    """
    Creates a JWT access token for the authenticated user.
    """
    return create_access_token(data={"sub": str(user.id)})
