from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: PostCreate, owner_id: int
    ) -> Post:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, author_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_announcements(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        return (
            db.query(self.model)
            .filter(Post.is_announcement == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        return (
            db.query(self.model)
            .filter(Post.author_id == author_id)
            .options(
                joinedload(Post.community),
                joinedload(Post.author),
                joinedload(Post.likes),
                joinedload(Post.comments)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_community(
        self, db: Session, *, community_id: int, skip: int = 0, limit: int = 100
    ) -> List[Post]:
        return (
            db.query(self.model)
            .filter(Post.community_id == community_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

post = CRUDPost(Post) 