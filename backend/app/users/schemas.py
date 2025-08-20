import uuid 
from pydantic import BaseModel , EmailStr , ConfigDict 

# --- User Base ---
class UserBase(BaseModel):
    """
        Base Schema for a user , containing common attributes 
    """
    email: EmailStr
    full_name: str | None = None 

# --- User Create --- 
class UserCreate(UserBase):
    """
        Schema for creating a new user.
    """
    pass
# --- User Public ---

class UserPublic(UserBase):
    """
        Public facing User Schema , safe , for the frontend 
    """
    id: uuid.UUID 
    is_active: bool 

    # --- Condig Mapping --- 
    model_config = ConfigDict(from_attributes=True)

