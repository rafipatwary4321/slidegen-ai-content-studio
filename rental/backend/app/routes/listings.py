from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import ListingCategory
from app.models.listing import Listing
from app.models.listing_lifestyle_profile import ListingLifestyleProfile
from app.models.lifestyle_profile import LifestyleProfile
from app.models.tourism_detail import TourismDetail
from app.models.user import User
from app.schemas.listing import (
    ListingCreate,
    ListingExploreItem,
    ListingRead,
    ListingSearchItem,
    ListingSearchResponse,
    ListingUpdate,
)
from app.schemas.tourism_detail import TourismDetailRead, TourismDetailUpsert
from app.services import listing_search
from app.services.matchmaking import calculate_match_score

router = APIRouter(prefix="/api/v1/listings", tags=["listings"])


@router.get(
    "/explore",
    response_model=list[ListingExploreItem],
    summary="Unified listing explore (category, price range, geo radius)",
)
def explore_listings(
    db: Session = Depends(get_db),
    category: ListingCategory | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    lat: float | None = Query(None, description="Reference latitude for radius filtering"),
    lon: float | None = Query(None, description="Reference longitude for radius filtering"),
    radius_km: float | None = Query(None, ge=0.1, le=500.0),
    user_id: int | None = Query(None, description="Logged-in user id for Bachelor match scoring"),
) -> list[ListingExploreItem]:
    stmt = select(Listing)
    price_expr = func.coalesce(Listing.price, Listing.price_daily)

    if category is not None:
        stmt = stmt.where(Listing.category == category)
    if min_price is not None:
        stmt = stmt.where(price_expr >= min_price)
    if max_price is not None:
        stmt = stmt.where(price_expr <= max_price)

    if radius_km is not None:
        if lat is None or lon is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="lat and lon are required when radius_km is provided",
            )
        dist = listing_search.haversine_distance_km(Listing.latitude, Listing.longitude, lat, lon)
        stmt = stmt.where(dist <= radius_km)

    stmt = stmt.order_by(Listing.id.desc())
    rows = list(db.scalars(stmt).all())
    user_profile = db.get(LifestyleProfile, user_id) if user_id is not None else None

    # Keep gear aliases in sync for frontend clarity.
    out: list[ListingExploreItem] = []
    for row in rows:
        if row.gear_available is None and row.available_gear is not None:
            row.gear_available = row.available_gear
        if row.available_gear is None and row.gear_available is not None:
            row.available_gear = row.gear_available
        match_score: float | None = None
        if row.category == ListingCategory.BACHELOR and user_profile is not None and row.lifestyle_profile_id:
            listing_profile = db.get(ListingLifestyleProfile, row.lifestyle_profile_id)
            if listing_profile is not None:
                match_score = calculate_match_score(
                    user_prefs={
                        "is_smoker": user_profile.is_smoker,
                        "sleep_cycle": user_profile.sleep_cycle,
                        "job_type": user_profile.job_type,
                    },
                    listing_prefs={
                        "is_smoker": listing_profile.is_smoker,
                        "sleep_cycle": listing_profile.sleep_cycle,
                        "job_type": listing_profile.job_type,
                    },
                )
        if row.category == ListingCategory.BACHELOR and user_profile is not None and match_score is None:
            match_score = 20.0
        out.append(ListingExploreItem(**row.__dict__, match_score=match_score))
    return out


@router.get(
    "/search",
    response_model=ListingSearchResponse,
    summary="Smart search (geo, category, tourism, Bachelor match, host reputation)",
)
def search_listings(
    db: Session = Depends(get_db),
    lat: float = Query(..., description="Search origin latitude"),
    lon: float = Query(..., description="Search origin longitude"),
    radius_km: float = Query(5.0, ge=0.1, le=500.0, description="Radius in kilometers"),
    category: ListingCategory | None = Query(
        None,
        description="Filter: Short-Stay, Bachelor, Family, Tourism",
    ),
    viewer_user_id: int | None = Query(
        None,
        description="Seeker user id; LifestyleProfile used for Bachelor compatibility_percent",
    ),
    home_stay: bool | None = Query(
        None,
        description="Tourism: home-stay style (amenities.home_stay or stay_type=home_stay)",
    ),
    local_guide: bool | None = Query(
        None,
        description="Tourism: require tourism_details.has_guide",
    ),
    adventure_gear: bool | None = Query(
        None,
        description="Tourism: require non-empty adventure_gear_rental on tourism_details",
    ),
    female_only: bool | None = Query(
        None,
        description="Only listings with amenities.female_only = true (Safety Mode)",
    ),
) -> ListingSearchResponse:
    """
    Geospatial search within `radius_km`, optional category and tourism filters.

    Results are ordered by **distance**, then by **host reputation_score** (descending).

    For **Bachelor** listings, pass `viewer_user_id` to get **compatibility_percent** (0–100)
    vs current mess members (host + active Confirmed stays).
    """
    try:
        stmt = listing_search.build_listing_search_statement(
            ref_lat=lat,
            ref_lon=lon,
            radius_km=radius_km,
            category=category,
            home_stay=home_stay,
            local_guide=local_guide,
            adventure_gear=adventure_gear,
            female_only=female_only,
        )
        rows = db.execute(stmt).all()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database query failed: {exc}",
        ) from exc

    listings = [row[0] for row in rows]
    distances = {row[0].id: float(row[1]) for row in rows}
    host_rep = {row[0].id: listing_search.reputation_to_float(row[2]) for row in rows}

    match_by_id = listing_search.bachelor_match_scores_for_listings(
        db, listings, viewer_user_id
    )

    items: list[ListingSearchItem] = []
    for L in listings:
        items.append(
            ListingSearchItem(
                id=L.id,
                title=L.title,
                category=L.category.value,
                latitude=L.latitude,
                longitude=L.longitude,
                distance_km=round(distances[L.id], 3),
                host_reputation_score=host_rep[L.id],
                compatibility_percent=(match_by_id.get(L.id) if L.category == ListingCategory.BACHELOR else None),
                match_score=(match_by_id.get(L.id) if L.category == ListingCategory.BACHELOR else None),
                female_only_host=listing_search.amenities_female_only(L.amenities),
                price_daily=listing_search.decimal_or_none(L.price_daily),
                price_monthly=listing_search.decimal_or_none(L.price_monthly),
            )
        )

    return ListingSearchResponse(items=items)


@router.post("", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)) -> Listing:
    if db.get(User, payload.owner_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner user not found")
    data = payload.model_dump()
    # Keep tourism gear aliases in sync (`gear_rental`, `gear_available`, `available_gear`).
    gear = data.get("gear_rental") or data.get("gear_available") or data.get("available_gear")
    data["gear_available"] = gear
    data["available_gear"] = gear
    data.pop("gear_rental", None)
    listing = Listing(**data)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.put("/{listing_id}/tourism-detail", response_model=TourismDetailRead)
def upsert_tourism_detail(
    listing_id: int,
    payload: TourismDetailUpsert,
    db: Session = Depends(get_db),
) -> TourismDetail:
    if db.get(Listing, listing_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    row = db.get(TourismDetail, listing_id)
    if row is None:
        row = TourismDetail(
            listing_id=listing_id,
            has_guide=payload.has_guide,
            local_food_available=payload.local_food_available,
            adventure_gear_rental=payload.adventure_gear_rental,
        )
        db.add(row)
    else:
        row.has_guide = payload.has_guide
        row.local_food_available = payload.local_food_available
        row.adventure_gear_rental = payload.adventure_gear_rental
    db.commit()
    db.refresh(row)
    return row


@router.get("/{listing_id}/tourism-detail", response_model=TourismDetailRead)
def get_tourism_detail(listing_id: int, db: Session = Depends(get_db)) -> TourismDetail:
    row = db.get(TourismDetail, listing_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourism detail not found")
    return row


@router.get("/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: int, db: Session = Depends(get_db)) -> Listing:
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    if listing.gear_available is None and listing.available_gear is not None:
        listing.gear_available = listing.available_gear
    if listing.available_gear is None and listing.gear_available is not None:
        listing.available_gear = listing.gear_available
    return listing


@router.patch("/{listing_id}", response_model=ListingRead)
def update_listing(
    listing_id: int,
    payload: ListingUpdate,
    db: Session = Depends(get_db),
) -> Listing:
    listing = db.get(Listing, listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    data = payload.model_dump(exclude_unset=True)
    if "gear_rental" in data:
        data["gear_available"] = data["gear_rental"]
        data["available_gear"] = data["gear_rental"]
        data.pop("gear_rental", None)
    elif "gear_available" in data and "available_gear" not in data:
        data["available_gear"] = data["gear_available"]
    elif "available_gear" in data and "gear_available" not in data:
        data["gear_available"] = data["available_gear"]

    for k, v in data.items():
        setattr(listing, k, v)
    db.commit()
    db.refresh(listing)
    return listing
