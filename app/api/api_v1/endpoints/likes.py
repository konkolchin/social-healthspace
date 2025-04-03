from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/post/{post_id}", response_model=schemas.Post)
def like_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Like a post.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if crud.like.get_by_user_and_post(db, user_id=current_user.id, post_id=post_id):
        raise HTTPException(status_code=400, detail="Post already liked")
    crud.like.create_with_owner(db=db, owner_id=current_user.id, post_id=post_id)
    return post

@router.delete("/post/{post_id}", response_model=schemas.Post)
def unlike_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Unlike a post.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    like = crud.like.get_by_user_and_post(db, user_id=current_user.id, post_id=post_id)
    if not like:
        raise HTTPException(status_code=400, detail="Post not liked")
    crud.like.remove(db=db, id=like.id)
    return post 