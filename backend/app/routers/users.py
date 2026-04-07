from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Follow, User
from app.schemas import FollowResponse, UserProfile
from app.services import user_profile


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserProfile)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profile(db, user)


@router.post("/{user_id}/follow", response_model=FollowResponse)
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    target = db.get(User, user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    follow = db.scalar(
        select(Follow).where(
            and_(Follow.follower_id == current_user.id, Follow.following_id == user_id)
        )
    )
    if follow is None:
        db.add(Follow(follower_id=current_user.id, following_id=user_id))
        db.commit()
    return FollowResponse(following_user_id=user_id, is_following=True)


@router.delete(
    "/{user_id}/follow", response_model=FollowResponse, status_code=status.HTTP_200_OK
)
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    follow = db.scalar(
        select(Follow).where(
            and_(Follow.follower_id == current_user.id, Follow.following_id == user_id)
        )
    )
    if follow is not None:
        db.delete(follow)
        db.commit()
    return FollowResponse(following_user_id=user_id, is_following=False)
