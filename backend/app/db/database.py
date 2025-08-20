from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings 

# --- Create the SQLAlchemy engine ---
engine = create_engine(settings.DATABASE_URL , pool_pre_ping=True)
# --- Create the SessionLocal ----
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
# --- Create the Base DB ----
Base = declarative_base()

def get_db():
    """
        FastAPI dependency that provides a database session to an endpoint 
    """
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
    

