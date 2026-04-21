from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status  # pylint: disable=import-error
from sqlalchemy import select  # pylint: disable=import-error
from sqlalchemy.orm import Session  # pylint: disable=import-error

from app.core.database import get_db
from app.models.enums import ListingCategory
from app.models.listing import Listing
from app.models.listing_lifestyle_profile import ListingLifestyleProfile
from app.models.lifestyle_profile import LifestyleProfile
from app.models.user import User
from app.schemas.listing_core import CoreListingCreate, CoreListingRead
from app.services.matchmaking import calculate_match_score

router = APIRouter(prefix="/listings", tags=["core-listings"])


@router.post("", response_model=CoreListingRead, status_code=status.HTTP_201_CREATED)
def create_core_listing(
    payload: CoreListingCreate,
    db: Session = Depends(get_db),
) -> Listing:
    if db.get(User, payload.owner_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner user not found")

    lifestyle_profile_id = payload.lifestyle_profile_id
    if payload.category == ListingCategory.BACHELOR:
        if lifestyle_profile_id is None and payload.lifestyle_profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bachelor listing requires lifestyle_profile_id or lifestyle_profile payload",
            )
        if payload.lifestyle_profile is not None:
            profile = ListingLifestyleProfile(**payload.lifestyle_profile.model_dump())
            db.add(profile)
            db.flush()
            lifestyle_profile_id = profile.id
        elif db.get(ListingLifestyleProfile, lifestyle_profile_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lifestyle profile not found",
            )

    listing = Listing(
        owner_id=payload.owner_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        latitude=payload.latitude,
        longitude=payload.longitude,
        category=payload.category,
        lifestyle_profile_id=lifestyle_profile_id,
        has_guide=payload.has_guide if payload.category == ListingCategory.TOURISM else False,
        gear_available=payload.gear_available if payload.category == ListingCategory.TOURISM else [],
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.get("", response_model=list[CoreListingRead])
def get_core_listings(
    db: Session = Depends(get_db),
    category: ListingCategory | None = Query(None),
    user_id: int | None = Query(None, description="Logged-in user id for Bachelor match scoring"),
) -> list[CoreListingRead]:
    stmt = select(Listing).order_by(Listing.id.desc())
    if category is not None:
        stmt = stmt.where(Listing.category == category)
    rows = list(db.scalars(stmt).all())

    user_profile = db.get(LifestyleProfile, user_id) if user_id is not None else None
    out: list[CoreListingRead] = []
    for row in rows:
        match_score: float | None = None
        if row.category == ListingCategory.BACHELOR and user_profile is not None and row.lifestyle_profile_id:
            lp = db.get(ListingLifestyleProfile, row.lifestyle_profile_id)
            if lp is not None:
                match_score = calculate_match_score(
                    user_prefs={
                        "is_smoker": user_profile.is_smoker,
                        "sleep_cycle": user_profile.sleep_cycle,
                        "job_type": user_profile.job_type,
                    },
                    listing_prefs={
                        "is_smoker": lp.is_smoker,
                        "sleep_cycle": lp.sleep_cycle,
                        "job_type": lp.job_type,
                    },
                )
        if row.category == ListingCategory.BACHELOR and user_profile is not None and match_score is None:
            match_score = 20.0

        out.append(
            CoreListingRead(
                id=row.id,
                owner_id=row.owner_id,
                title=row.title,
                description=row.description,
                price=row.price,
                latitude=row.latitude,
                longitude=row.longitude,
                category=row.category,
                lifestyle_profile_id=row.lifestyle_profile_id,
                match_score=match_score,
                has_guide=row.has_guide,
                gear_available=row.gear_available,
            )
        )
    return out

