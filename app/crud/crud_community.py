from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.models.community import Community, community_members
from app.models.user import User
from app.schemas.community import CommunityCreate, CommunityUpdate
from app.core.security import get_password_hash
from slugify import slugify

class CRUDCommunity(CRUDBase[Community, CommunityCreate, CommunityUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CommunityCreate, owner_id: int
    ) -> Community:
        obj_in_data = jsonable_encoder(obj_in)
        # Create slug from name
        slug = slugify(obj_in_data["name"])
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while db.query(Community).filter(Community.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        db_obj = Community(**obj_in_data, slug=slug, created_by_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add owner as member
        self.add_member(db=db, community_id=db_obj.id, user_id=owner_id)
        return db_obj

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Community]:
        return db.query(Community).filter(Community.slug == slug).first()

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Community]:
        return (
            db.query(Community)
            .filter(Community.created_by_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def add_member(
        self, db: Session, *, community_id: int, user_id: int
    ) -> Community:
        community = db.query(Community).filter(Community.id == community_id).first()
        if not community:
            return None
        
        # Check if already a member
        is_member = db.query(community_members).filter(
            community_members.c.community_id == community_id,
            community_members.c.user_id == user_id
        ).first()
        
        if not is_member:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                community.members.append(user)
                db.commit()
                db.refresh(community)
        
        return community

    def remove_member(
        self, db: Session, *, community_id: int, user_id: int
    ) -> Community:
        community = db.query(Community).filter(Community.id == community_id).first()
        if not community:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        if user and user in community.members:
            community.members.remove(user)
            db.commit()
            db.refresh(community)
        
        return community

    def get_member_count(
        self, db: Session, *, community_id: int
    ) -> int:
        return db.query(func.count(community_members.c.user_id))\
            .filter(community_members.c.community_id == community_id)\
            .scalar()

    def is_member(
        self, db: Session, *, community_id: int, user_id: int
    ) -> bool:
        return db.query(community_members)\
            .filter(
                community_members.c.community_id == community_id,
                community_members.c.user_id == user_id
            ).first() is not None

    def get_user_communities(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Community]:
        return (
            db.query(Community)
            .join(community_members)
            .filter(community_members.c.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_communities(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Community]:
        return (
            db.query(Community)
            .filter(Community.name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

community = CRUDCommunity(Community)
