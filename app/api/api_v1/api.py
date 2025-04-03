from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    users,
    posts,
    comments,
    likes,
    communities
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(communities.router, prefix="/communities", tags=["communities"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(likes.router, prefix="/likes", tags=["likes"]) 