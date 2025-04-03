from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# Temporary fix until email-validator works
class UserBase(BaseModel):
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    name: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class UserResponse(BaseModel):
    user: User
    access_token: str
    token_type: str