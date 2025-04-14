from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.Community)
def create_community(
    *,
    db: Session = Depends(deps.get_db),
    community_in: schemas.CommunityCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new community.
    """
    community = crud.community.create_with_owner(
        db=db, obj_in=community_in, owner_id=current_user.id
    )
    return community

@router.get("/", response_model=List[schemas.Community])
def list_communities(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
    search: Optional[str] = Query(None, min_length=3, max_length=50),
    response: Response,
) -> Any:
    """
    Retrieve communities.
    """
    # Set CORS headers
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:5174",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept"
    })

    if search:
        communities = crud.community.search_communities(
            db=db, query=search, skip=skip, limit=limit
        )
    else:
        communities = crud.community.get_multi(db, skip=skip, limit=limit)
    
    # Format response
    formatted_communities = []
    for community in communities:
        is_member = crud.community.is_member(
            db=db, community_id=community.id, user_id=current_user.id
        )
        is_admin = community.created_by_id == current_user.id
        members_count = crud.community.get_member_count(
            db=db, community_id=community.id
        )
        
        formatted_communities.append({
            "id": community.id,
            "name": community.name,
            "description": community.description,
            "is_private": community.is_private,
            "slug": community.slug,
            "created_at": community.created_at,
            "created_by_id": community.created_by_id,
            "is_member": is_member,
            "is_admin": is_admin,
            "members_count": members_count
        })
    
    return formatted_communities

@router.get("/my", response_model=List[schemas.Community])
def list_my_communities(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve communities where user is member.
    """
    communities = crud.community.get_user_communities(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    for community in communities:
        community.is_member = True
        community.is_admin = community.created_by_id == current_user.id
        community.members_count = crud.community.get_member_count(
            db=db, community_id=community.id
        )
    return communities

@router.get("/{slug}", response_model=schemas.CommunityWithMembers)
def get_community(
    *,
    db: Session = Depends(deps.get_db),
    slug: str,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get community by slug.
    """
    community = crud.community.get_by_slug(db=db, slug=slug)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    community.is_member = crud.community.is_member(
        db=db, community_id=community.id, user_id=current_user.id
    )
    community.is_admin = community.created_by_id == current_user.id
    community.members_count = crud.community.get_member_count(
        db=db, community_id=community.id
    )
    return community

@router.put("/{community_id}", response_model=schemas.Community)
def update_community(
    *,
    db: Session = Depends(deps.get_db),
    community_id: int,
    community_in: schemas.CommunityUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update community.
    """
    community = crud.community.get(db=db, id=community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    if community.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    community = crud.community.update(db=db, db_obj=community, obj_in=community_in)
    return community

@router.post("/{community_id}/members", response_model=schemas.Community)
def join_community(
    *,
    db: Session = Depends(deps.get_db),
    community_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Join community.
    """
    community = crud.community.get(db=db, id=community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    if community.is_private and community.created_by_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="This is a private community. Contact the administrator."
        )
    
    community = crud.community.add_member(
        db=db, community_id=community_id, user_id=current_user.id
    )
    return community

@router.delete("/{community_id}/members", response_model=schemas.Community)
def leave_community(
    *,
    db: Session = Depends(deps.get_db),
    community_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Leave community.
    """
    community = crud.community.get(db=db, id=community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    if community.created_by_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Community owner cannot leave the community"
        )
    
    community = crud.community.remove_member(
        db=db, community_id=community_id, user_id=current_user.id
    )
    return community

@router.delete("/{community_id}", response_model=schemas.Community)
def delete_community(
    *,
    db: Session = Depends(deps.get_db),
    community_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete community.
    """
    community = crud.community.get(db=db, id=community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    if community.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    community = crud.community.remove(db=db, id=community_id)
    return community
