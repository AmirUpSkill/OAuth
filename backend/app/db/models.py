import uuid 
from sqlalchemy import Column , String , Boolean 
from sqlalchemy.dialects.postgresql import UUID 
from app.db.database import Base 

class User(Base):
    """
    Database model for a User.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)