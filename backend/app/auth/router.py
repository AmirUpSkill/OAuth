from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.config import settings
from app.auth.service import (
    get_google_authorization_url,
    handle_google_callback,
    create_user_token,
)
from app.auth.schemas import AuthURL, LoginResponse
from app.core.security import TokenDep
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Get Google Login URL --- 
@router.get("/login/google", response_model=AuthURL)
def google_login():
    """
    Returns the Google OAuth authorization URL for frontend to redirect users.
    
    Returns:
        AuthURL: Contains the authorization_url for Google OAuth
    """
    try:
        # Use environment variable for callback URL
        redirect_uri = f"{settings.BACKEND_URL}/api/v1/auth/callback/google"
        auth_url = get_google_authorization_url(redirect_uri)
        return AuthURL(authorization_url=auth_url)
    except Exception as e:
        logger.error(f"Failed to generate Google login URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authorization URL"
        )
# --- Handle Google Callback --- 
@router.get("/callback/google")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handles the callback from Google OAuth.
    
    This endpoint:
    1. Exchanges the authorization code for tokens
    2. Retrieves user info from Google
    3. Creates or updates user in database
    4. Sets secure authentication cookie
    5. Redirects user to frontend dashboard
    
    Args:
        request: FastAPI request object containing OAuth callback data
        db: Database session
    
    Returns:
        RedirectResponse: Redirects to frontend with success/error status
    """
    try:
        user = await handle_google_callback(request, db)
        token = create_user_token(user)
        
        # Create redirect response to frontend
        redirect_response = RedirectResponse(
            url=f"{settings.FRONTEND_URL}/dashboard",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
        
        # Set secure cookie with token
        redirect_response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",  # Only secure in production
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
            path="/",
            domain=settings.COOKIE_DOMAIN if hasattr(settings, 'COOKIE_DOMAIN') else None
        )
        
        logger.info(f"User {user.email} successfully authenticated via Google OAuth")
        return redirect_response
        
    except HTTPException:
        # Re-raise HTTP exceptions (these are already handled by the service layer)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in Google callback: {str(e)}")
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error=authentication_failed",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

# --- Validate Token --- 
@router.get("/validate", response_model=dict)
async def validate_token(token_data: TokenDep):
    """
    Validates the current access token and returns token payload.
    
    This endpoint can be used by the frontend to:
    - Check if user is still authenticated
    - Get user ID from token
    - Validate token before making protected requests
    
    Args:
        token_data: Decoded JWT token data
    
    Returns:
        dict: Token payload containing user information
    """
    return {
        "valid": True,
        "user_id": token_data.get("sub"),
        "expires_at": token_data.get("exp")
    }

# --- Logout --- 
@router.post("/logout")
def logout(response: Response, token_data: TokenDep = None):
    """
    Logs out the user by clearing the access token cookie.
    
    Args:
        response: FastAPI response object
        token_data: Optional token data (if user is authenticated)
    
    Returns:
        dict: Success message
    """
    try:
        # Clear the access token cookie
        response.delete_cookie(
            key="access_token",
            path="/",
            domain=settings.COOKIE_DOMAIN if hasattr(settings, 'COOKIE_DOMAIN') else None,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax"
        )
        
        if token_data:
            user_id = token_data.get("sub")
            logger.info(f"User {user_id} successfully logged out")
        
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        # Still return success even if logging fails
        return {"message": "Successfully logged out"}
