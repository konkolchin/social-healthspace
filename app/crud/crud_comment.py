from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CommentCreate, owner_id: int, post_id: int
    ) -> Comment:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, author_id=owner_id, post_id=post_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_post(
        self, db: Session, *, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

comment = CRUDComment(Comment) 