from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from decimal import Decimal

from sqlalchemy import Select, and_, func, or_, select, text
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.enums import BookingStatus, ListingCategory, SleepCycle
from app.models.listing import Listing
from app.models.lifestyle_profile import LifestyleProfile
from app.models.tourism_detail import TourismDetail
from app.models.user import User


def haversine_distance_km(lat_col, lon_col, ref_lat: float, ref_lon: float):
    """Great-circle distance (km) in PostgreSQL using listing coordinates."""
    rlat = func.radians(ref_lat)
    rlon = func.radians(ref_lon)
    return (
        6371.0
        * func.acos(
            func.least(
                1.0,
                func.greatest(
                    -1.0,
                    func.cos(rlat)
                    * func.cos(func.radians(lat_col))
                    * (func.cos(func.radians(lon_col) - rlon))
                    + func.sin(rlat) * func.sin(func.radians(lat_col)),
                ),
            )
        )
    )


def _adventure_gear_available_clause() -> text:
    """
    PostgreSQL: tourism_details row has non-empty JSON for adventure_gear_rental.
    """
    return text(
        "tourism_details.adventure_gear_rental IS NOT NULL "
        "AND tourism_details.adventure_gear_rental::text NOT IN ('null', '{}', '[]')"
    )


def amenities_female_only(amenities: dict | list | None) -> bool:
    return isinstance(amenities, dict) and amenities.get("female_only") is True


def build_listing_search_statement(
    *,
    ref_lat: float,
    ref_lon: float,
    radius_km: float,
    category: ListingCategory | None,
    home_stay: bool | None,
    local_guide: bool | None,
    adventure_gear: bool | None,
    female_only: bool | None,
) -> Select:
    """
    Listings within radius, optional category/tourism filters, joined to host for reputation sort.
    Order: distance ascending, then host reputation_score descending.
    """
    dist = haversine_distance_km(Listing.latitude, Listing.longitude, ref_lat, ref_lon)
    stmt: Select = (
        select(Listing, dist.label("distance_km"), User.reputation_score)
        .join(User, User.id == Listing.owner_id)
        .where(dist <= radius_km)
    )

    if category is not None:
        stmt = stmt.where(Listing.category == category)

    if female_only is True:
        stmt = stmt.where(
            Listing.amenities.isnot(None),
            Listing.amenities.contains({"female_only": True}),
        )

    if home_stay is True:
        home_expr = or_(
            Listing.amenities.contains({"home_stay": True}),
            Listing.amenities["stay_type"].as_string() == "home_stay",
        )
        stmt = stmt.where(
            Listing.category == ListingCategory.TOURISM,
            Listing.amenities.isnot(None),
            home_expr,
        )

    if local_guide is True or adventure_gear is True:
        stmt = stmt.join(TourismDetail, TourismDetail.listing_id == Listing.id)
        tourism_preds = []
        if local_guide is True:
            tourism_preds.append(TourismDetail.has_guide.is_(True))
        if adventure_gear is True:
            tourism_preds.append(_adventure_gear_available_clause())
        stmt = stmt.where(and_(*tourism_preds))

    stmt = stmt.order_by(dist.asc(), User.reputation_score.desc().nulls_last())
    return stmt


def _sleep_cycle_points(a: SleepCycle, b: SleepCycle) -> float:
    order = {
        SleepCycle.EARLY_BIRD: 0,
        SleepCycle.NORMAL: 1,
        SleepCycle.NIGHT_OWL: 2,
    }
    d = abs(order[a] - order[b])
    if d == 0:
        return 25.0
    if d == 1:
        return 15.0
    return 5.0


def calculate_match_score(
    user_profile: LifestyleProfile,
    mess_profile: LifestyleProfile,
) -> float:
    """
    Compatibility percentage (0–100) between the seeker's LifestyleProfile and one mess member's profile.
    Weights: smoking match, sleep cycle proximity, cleanliness proximity, job_type similarity.
    """
    score = 0.0
    score += 25.0 if user_profile.is_smoker == mess_profile.is_smoker else 0.0
    score += _sleep_cycle_points(user_profile.sleep_cycle, mess_profile.sleep_cycle)

    diff = abs(user_profile.cleanliness_score - mess_profile.cleanliness_score)
    score += 25.0 * (1.0 - min(diff / 9.0, 1.0))

    vj = (user_profile.job_type or "").strip().lower()
    mj = (mess_profile.job_type or "").strip().lower()
    if vj and mj:
        score += 25.0 if vj == mj else 0.0
    elif not vj and not mj:
        score += 25.0
    else:
        score += 10.0

    return round(score, 2)


def lifestyle_pair_score(viewer: LifestyleProfile, member: LifestyleProfile) -> float:
    """Backwards-compatible alias for [calculate_match_score]."""
    return calculate_match_score(viewer, member)


def _mess_member_user_ids(
    db: Session,
    listing_id: int,
    owner_id: int,
    today: date,
    exclude_user_id: int | None,
) -> set[int]:
    rows = db.scalars(
        select(Booking.user_id).where(
            Booking.listing_id == listing_id,
            Booking.status == BookingStatus.CONFIRMED,
            Booking.check_in <= today,
            Booking.check_out >= today,
        )
    ).all()
    members = set(rows) | {owner_id}
    if exclude_user_id is not None:
        members.discard(exclude_user_id)
    return members


def bachelor_match_scores_for_listings(
    db: Session,
    listings: Iterable[Listing],
    viewer_user_id: int | None,
) -> dict[int, float | None]:
    """
    For Bachelor listings: average compatibility % between the viewer and current mess members
    (host + users with an active Confirmed booking on that listing).
    """
    bachelor = [L for L in listings if L.category == ListingCategory.BACHELOR]
    out: dict[int, float | None] = {L.id: None for L in bachelor}

    if viewer_user_id is None or not bachelor:
        return out

    viewer = db.get(LifestyleProfile, viewer_user_id)
    if viewer is None:
        return out

    today = date.today()
    listing_member_ids: dict[int, set[int]] = {}
    all_ids: set[int] = set()

    for L in bachelor:
        mids = _mess_member_user_ids(db, L.id, L.owner_id, today, viewer_user_id)
        listing_member_ids[L.id] = mids
        all_ids |= mids

    if not all_ids:
        return out

    profiles = {
        p.user_id: p
        for p in db.scalars(
            select(LifestyleProfile).where(LifestyleProfile.user_id.in_(all_ids))
        ).all()
    }

    for L in bachelor:
        mids = listing_member_ids[L.id]
        member_profiles = [profiles[uid] for uid in mids if uid in profiles]
        if not member_profiles:
            out[L.id] = None
            continue
        scores = [calculate_match_score(viewer, mp) for mp in member_profiles]
        out[L.id] = round(sum(scores) / len(scores), 2)

    return out


def decimal_or_none(v: Decimal | None) -> float | None:
    if v is None:
        return None
    return float(v)


def reputation_to_float(v: Decimal | float | None) -> float:
    if v is None:
        return 0.0
    return float(v)
