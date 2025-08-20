from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import TokenDep
from app.users.service import get_user_by_id
from app.users.schemas import UserPublic
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me" , response_model=UserPublic)
def get_current_user(
    token_data: TokenDep , 
    db: Session = Depends(get_db)
):
    """
        Returns the currently authenticated user's profile 
    """
    # --- get user id ---
    user_id = uuid.UUID(token_data["sub"])
    user = get_user_by_id(db, user_id)
    # --- check user ---
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
