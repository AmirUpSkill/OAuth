import uuid
from sqlalchemy.orm import Session
from app.users.service import create_user, get_user_by_email, get_user_by_id
from app.users.schemas import UserCreate


def test_create_user(db_session: Session):
    """Test creating a new user."""
    user_in = UserCreate(email="test@example.com", full_name="Test User")
    user = create_user(db_session, user_in)
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.id is not None
    assert user.is_active is True  # Should be True by default


def test_get_user_by_email(db_session: Session):
    """Test retrieving a user by email address."""
    user_in = UserCreate(email="findme@example.com", full_name="Finder")
    created = create_user(db_session, user_in)
    
    found = get_user_by_email(db_session, "findme@example.com")
    
    assert found is not None
    assert found.id == created.id
    assert found.email == "findme@example.com"


def test_get_user_by_email_not_found(db_session: Session):
    """Test that get_user_by_email returns None for non-existent user."""
    found = get_user_by_email(db_session, "nonexistent@example.com")
    assert found is None


def test_get_user_by_id(db_session: Session):
    """Test retrieving a user by ID."""
    user_in = UserCreate(email="byid@example.com", full_name="By ID")
    created = create_user(db_session, user_in)
    
    found = get_user_by_id(db_session, created.id)
    
    assert found is not None
    assert found.email == "byid@example.com"
    assert found.full_name == "By ID"


def test_get_user_by_id_not_found(db_session: Session):
    """Test that get_user_by_id returns None for non-existent user."""
    fake_id = uuid.uuid4()
    found = get_user_by_id(db_session, fake_id)
    assert found is None
