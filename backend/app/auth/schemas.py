from pydantic import BaseModel , HttpUrl 

# --- Schema Layer ---
class AuthURL(BaseModel):
    """
        Schema for the response that provides the Google OAuth 
        authorization URL . 
    """
    authorization_url: HttpUrl 

