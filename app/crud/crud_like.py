from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.like import Like
from app.schemas.like import LikeCreate, LikeUpdate

class CRUDLike(CRUDBase[Like, LikeCreate, LikeUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: LikeCreate, owner_id: int, post_id: int
    ) -> Like:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, user_id=owner_id, post_id=post_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_and_post(
        self, db: Session, *, user_id: int, post_id: int
    ) -> Optional[Like]:
        return (
            db.query(self.model)
            .filter(Like.user_id == user_id, Like.post_id == post_id)
            .first()
        )

    def get_by_post(
        self, db: Session, *, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Like]:
        return (
            db.query(self.model)
            .filter(Like.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Like]:
        return (
            db.query(self.model)
            .filter(Like.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

like = CRUDLike(Like) 