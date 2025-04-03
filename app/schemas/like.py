from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikeUpdate(LikeBase):
    pass

class LikeInDBBase(LikeBase):
    id: Optional[int] = None
    user_id: Optional[int] = None
    post_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Like(LikeInDBBase):
    pass 