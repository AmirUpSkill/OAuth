from sqlalchemy.orm import Session
from app.db.models import User
from app.users.schemas import UserCreate
import uuid 

def get_user_by_email(db: Session , email: str) -> User | None:
    """
        Fetch a user by email 
        Returns None if Not Found 
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session , user_id: uuid.UUID) -> User | None:
    """
        Fetch a user by ID 
        Returns None if Not Found 
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session , user: UserCreate) -> User:
    """
        Create a new user in the database 
    """
    db_user = User(
        email = user.email,
        full_name = user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

