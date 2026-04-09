from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import ListingCategory
from app.models.listing import Listing
from app.models.tourism_detail import TourismDetail
from app.models.user import User
from app.schemas.listing import (
    ListingCreate,
    ListingRead,
    ListingSearchItem,
    ListingSearchResponse,
    ListingUpdate,
)
from app.schemas.tourism_detail import TourismDetailRead, TourismDetailUpsert
from app.services import listing_search

router = APIRouter(prefix="/api/v1/listings", tags=["listings"])


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
                compatibility_percent=(
                    match_by_id.get(L.id) if L.category == ListingCategory.BACHELOR else None
                ),
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
    listing = Listing(**payload.model_dump())
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
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(listing, k, v)
    db.commit()
    db.refresh(listing)
    return listing
