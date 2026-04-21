"""
Populate UrbanRelief with core demo listings for all pillars.

Creates:
- 2 Bachelor messes (students, professionals)
- 2 Tourism spots (Sylhet, Sajek) with guides
- 2 Short-stay apartments in Dhaka
- 1 Family house

Run from `backend/`:
  .\\.venv\\Scripts\\python scripts\\seed_urbanrelief.py
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))
load_dotenv(BACKEND / ".env")

from app.core.database import SessionLocal  # noqa: E402  # pylint: disable=import-error
from app.models.enums import ListingCategory, SleepCycle, UserRole  # noqa: E402  # pylint: disable=import-error
from app.models.listing import Listing  # noqa: E402  # pylint: disable=import-error
from app.models.listing_lifestyle_profile import ListingLifestyleProfile  # noqa: E402  # pylint: disable=import-error
from app.models.user import User  # noqa: E402  # pylint: disable=import-error


def _get_or_create_host(db, *, full_name: str, phone: str, email: str) -> User:
    row = db.scalars(select(User).where(User.email == email)).first()
    if row is not None:
        return row
    row = User(
        full_name=full_name,
        phone=phone,
        email=email,
        role=UserRole.HOST,
        reputation_score=Decimal("4.50"),
    )
    db.add(row)
    db.flush()
    return row


def _add_listing_if_missing(db, listing: Listing) -> None:
    exists = db.scalars(select(Listing).where(Listing.title == listing.title)).first()
    if exists is None:
        db.add(listing)


def main() -> None:
    if SessionLocal is None:
        raise SystemExit("DATABASE_URL is not set.")
    db = SessionLocal()
    try:
        host_student = _get_or_create_host(
            db,
            full_name="Host Student Mess",
            phone="+8801701000001",
            email="host.student@urbanrelief.demo",
        )
        host_prof = _get_or_create_host(
            db,
            full_name="Host Professional Mess",
            phone="+8801701000002",
            email="host.pro@urbanrelief.demo",
        )
        host_tour = _get_or_create_host(
            db,
            full_name="Host Tourism",
            phone="+8801701000003",
            email="host.tour@urbanrelief.demo",
        )
        host_stay = _get_or_create_host(
            db,
            full_name="Host Short Stay",
            phone="+8801701000004",
            email="host.stay@urbanrelief.demo",
        )
        host_family = _get_or_create_host(
            db,
            full_name="Host Family",
            phone="+8801701000005",
            email="host.family@urbanrelief.demo",
        )

        lp_students = ListingLifestyleProfile(
            is_smoker=False,
            job_type="student",
            sleep_cycle=SleepCycle.NIGHT_OWL,
        )
        lp_prof = ListingLifestyleProfile(
            is_smoker=False,
            job_type="professional",
            sleep_cycle=SleepCycle.EARLY_BIRD,
        )
        db.add_all([lp_students, lp_prof])
        db.flush()

        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_student.id,
                title="Dhanmondi Student Bachelor Mess",
                description="Affordable student-friendly bachelor mess near universities.",
                category=ListingCategory.BACHELOR,
                latitude=23.7461,
                longitude=90.3742,
                price=Decimal("8500.00"),
                lifestyle_profile_id=lp_students.id,
                amenities={"wifi": True, "study_area": True},
            ),
        )
        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_prof.id,
                title="Gulshan Professional Bachelor Mess",
                description="Quiet and clean bachelor mess for working professionals.",
                category=ListingCategory.BACHELOR,
                latitude=23.7925,
                longitude=90.4078,
                price=Decimal("14000.00"),
                lifestyle_profile_id=lp_prof.id,
                amenities={"wifi": True, "generator": True},
            ),
        )

        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_tour.id,
                title="Sylhet Tea Garden Eco Stay",
                description="Tourism stay in Sylhet with local guide support.",
                category=ListingCategory.TOURISM,
                latitude=24.8949,
                longitude=91.8687,
                price=Decimal("3200.00"),
                price_daily=Decimal("3200.00"),
                has_guide=True,
                guide_price=Decimal("900.00"),
                gear_available=[
                    {"name": "hiking boots", "price": 300},
                    {"name": "tent", "price": 700},
                ],
                available_gear=[
                    {"name": "hiking boots", "price": 300},
                    {"name": "tent", "price": 700},
                ],
                amenities={"home_stay": True, "local_food": True},
            ),
        )
        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_tour.id,
                title="Sajek Valley Adventure Cabin",
                description="Hill-view cabin in Sajek with guide and rental gear.",
                category=ListingCategory.TOURISM,
                latitude=23.3817,
                longitude=92.2938,
                price=Decimal("3600.00"),
                price_daily=Decimal("3600.00"),
                has_guide=True,
                guide_price=Decimal("1000.00"),
                gear_available=[
                    {"name": "trekking pole", "price": 200},
                    {"name": "camping tent", "price": 800},
                ],
                available_gear=[
                    {"name": "trekking pole", "price": 200},
                    {"name": "camping tent", "price": 800},
                ],
                amenities={"home_stay": True, "campfire": True},
            ),
        )

        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_stay.id,
                title="Banani Short-stay Studio",
                description="Modern furnished studio for short urban trips.",
                category=ListingCategory.SHORT_STAY,
                latitude=23.7937,
                longitude=90.4066,
                price=Decimal("4200.00"),
                price_daily=Decimal("4200.00"),
                amenities={"wifi": True, "parking": True},
            ),
        )
        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_stay.id,
                title="Mirpur Cozy Short-stay Flat",
                description="Budget short-stay flat with essentials for travelers.",
                category=ListingCategory.SHORT_STAY,
                latitude=23.8223,
                longitude=90.3654,
                price=Decimal("2800.00"),
                price_daily=Decimal("2800.00"),
                amenities={"wifi": True, "kitchen": True},
            ),
        )

        _add_listing_if_missing(
            db,
            Listing(
                owner_id=host_family.id,
                title="Uttara Family House",
                description="Spacious family home with 3 bedrooms and kitchen.",
                category=ListingCategory.FAMILY,
                latitude=23.8759,
                longitude=90.3795,
                price=Decimal("6800.00"),
                price_daily=Decimal("6800.00"),
                amenities={"kids_friendly": True, "parking": True},
            ),
        )

        db.commit()
        print("UrbanRelief demo seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

