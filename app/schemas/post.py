from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from .user import User
from .comment import Comment
from .community import CommunityMinimal

class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_announcement: Optional[bool] = False

class PostCreate(PostBase):
    title: str
    content: str
    community_id: Optional[int] = None

class PostUpdate(PostBase):
    pass

class PostInDBBase(PostBase):
    id: Optional[int] = None
    author_id: Optional[int] = None
    community_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Post(PostInDBBase):
    author: Optional[User] = None
    community: Optional[CommunityMinimal] = None
    likes_count: Optional[int] = 0
    comments_count: Optional[int] = 0
    is_liked: Optional[bool] = False

class PostWithComments(Post):
    comments: List[Comment] = []

class PostInDB(PostInDBBase):
    pass 