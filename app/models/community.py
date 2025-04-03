from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Community(Base):
    __tablename__ = "communities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by = relationship("User", back_populates="owned_communities")
    members = relationship(
        "User",
        secondary="community_members",
        back_populates="communities"
    )
    posts = relationship("Post", back_populates="community", cascade="all, delete-orphan")

# Association table for community members
community_members = Table(
    "community_members",
    Base.metadata,
    Column("community_id", Integer, ForeignKey("communities.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)