from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .user import UserBase

class CommunityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    is_private: bool = False

class CommunityCreate(CommunityBase):
    pass

class CommunityUpdate(CommunityBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_private: Optional[bool] = None

class CommunityInDB(CommunityBase):
    id: int
    slug: str
    created_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True

class Community(CommunityInDB):
    members_count: int = 0
    created_by: Optional["UserBase"] = None
    is_member: bool = False
    is_admin: bool = False

    class Config:
        from_attributes = True

class CommunityWithMembers(Community):
    members: List["UserBase"] = []

    class Config:
        from_attributes = True

# For handling member operations
class CommunityMemberAdd(BaseModel):
    user_id: int

class CommunityMemberRemove(BaseModel):
    user_id: int

# For response models that need minimal community info
class CommunityMinimal(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True
