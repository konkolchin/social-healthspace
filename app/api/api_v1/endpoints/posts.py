from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.PostWithComments])
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve posts.
    """
    posts = crud.post.get_multi(db, skip=skip, limit=limit)
    for post in posts:
        post.likes_count = len(post.likes)
        post.is_liked = any(like.user_id == current_user.id for like in post.likes)
    return posts

@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.PostCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new post.
    """
    post = crud.post.create_with_owner(
        db=db, obj_in=post_in, owner_id=current_user.id
    )
    return post

@router.get("/announcements", response_model=List[schemas.Post])
def read_announcements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve announcements.
    """
    posts = crud.post.get_announcements(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.PostWithComments)
def read_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get post by ID.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes_count = len(post.likes)
    post.is_liked = any(like.user_id == current_user.id for like in post.likes)
    return post

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    post_in: schemas.PostUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a post.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = crud.post.update(db=db, db_obj=post, obj_in=post_in)
    return post

@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a post.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    post = crud.post.remove(db=db, id=post_id)
    return post 