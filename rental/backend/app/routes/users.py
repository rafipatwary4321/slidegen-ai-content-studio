from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import NidStatus
from app.models.lifestyle_profile import LifestyleProfile
from app.models.user import User
from app.schemas.lifestyle_profile import LifestyleProfileRead, LifestyleProfileUpsert
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    user = User(
        full_name=payload.full_name,
        phone=payload.phone,
        email=payload.email,
        role=payload.role,
        nid_status=payload.nid_status or NidStatus.UNVERIFIED,
        reputation_score=payload.reputation_score if payload.reputation_score is not None else Decimal("0"),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone or email already registered",
        ) from exc
    db.refresh(user)
    return user


@router.put("/{user_id}/lifestyle-profile", response_model=LifestyleProfileRead)
def upsert_lifestyle_profile(
    user_id: int,
    payload: LifestyleProfileUpsert,
    db: Session = Depends(get_db),
) -> LifestyleProfile:
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    row = db.get(LifestyleProfile, user_id)
    if row is None:
        row = LifestyleProfile(
            user_id=user_id,
            is_smoker=payload.is_smoker,
            job_type=payload.job_type,
            sleep_cycle=payload.sleep_cycle,
            cleanliness_score=payload.cleanliness_score,
        )
        db.add(row)
    else:
        row.is_smoker = payload.is_smoker
        row.job_type = payload.job_type
        row.sleep_cycle = payload.sleep_cycle
        row.cleanliness_score = payload.cleanliness_score
    db.commit()
    db.refresh(row)
    return row


@router.get("/{user_id}/lifestyle-profile", response_model=LifestyleProfileRead)
def get_lifestyle_profile(user_id: int, db: Session = Depends(get_db)) -> LifestyleProfile:
    row = db.get(LifestyleProfile, user_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lifestyle profile not found")
    return row


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(user, k, v)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone or email conflict",
        ) from exc
    db.refresh(user)
    return user
