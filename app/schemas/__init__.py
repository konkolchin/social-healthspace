from .user import User, UserCreate, UserUpdate, UserInDB, UserBase
from .token import Token, TokenPayload
from .post import Post, PostCreate, PostUpdate, PostInDB, PostWithComments
from .comment import Comment, CommentCreate, CommentUpdate
from .like import Like, LikeCreate
from .community import (
    Community,
    CommunityCreate,
    CommunityUpdate,
    CommunityInDB,
    CommunityWithMembers,
    CommunityMemberAdd,
    CommunityMemberRemove,
    CommunityMinimal
)

# Export these classes to be available directly from app.schemas
__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserBase",
    "Token",
    "TokenPayload",
    "Post",
    "PostCreate",
    "PostUpdate",
    "PostInDB",
    "PostWithComments",
    "Comment",
    "CommentCreate",
    "CommentUpdate",
    "Like",
    "LikeCreate",
    # Add Community schemas
    "Community",
    "CommunityCreate",
    "CommunityUpdate",
    "CommunityInDB",
    "CommunityWithMembers",
    "CommunityMemberAdd",
    "CommunityMemberRemove",
    "CommunityMinimal"
]
