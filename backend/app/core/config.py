from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Settings class to manage environment variables.
    Pydantic will automatically read variables from the .env file.
    """
    # Database
    DATABASE_URL: str
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth 2.0
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # URLs
    BACKEND_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Environment
    ENVIRONMENT: str = "development"
    COOKIE_DOMAIN: str = None
    
    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    The @lru_cache decorator ensures the .env file is read only once,
    improving performance.
    """
    return Settings()


# Create a single instance of settings to be used across the application
settings = get_settings()

