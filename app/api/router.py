from fastapi import APIRouter
from app.api.endpoints import auth, users, communities, posts, comments

router = APIRouter()

# Include all API endpoints
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(communities.router, prefix="/communities", tags=["communities"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(comments.router, prefix="/comments", tags=["comments"]) 