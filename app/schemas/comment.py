from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    content: Optional[str] = None

class CommentCreate(CommentBase):
    content: str

class CommentUpdate(CommentBase):
    pass

class CommentInDBBase(CommentBase):
    id: Optional[int] = None
    author_id: Optional[int] = None
    post_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Comment(CommentInDBBase):
    pass 