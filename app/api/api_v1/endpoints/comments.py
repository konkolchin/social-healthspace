from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/post/{post_id}", response_model=List[schemas.Comment])
def read_comments(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve comments for a post.
    """
    comments = crud.comment.get_by_post(db, post_id=post_id, skip=skip, limit=limit)
    return comments

@router.post("/post/{post_id}", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    comment_in: schemas.CommentCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new comment.
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = crud.comment.create_with_owner(
        db=db, obj_in=comment_in, owner_id=current_user.id, post_id=post_id
    )
    return comment

@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    comment_in: schemas.CommentUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a comment.
    """
    comment = crud.comment.get(db=db, id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.comment.update(db=db, db_obj=comment, obj_in=comment_in)
    return comment

@router.delete("/{comment_id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a comment.
    """
    comment = crud.comment.get(db=db, id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    comment = crud.comment.remove(db=db, id=comment_id)
    return comment 