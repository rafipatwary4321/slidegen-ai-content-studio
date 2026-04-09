"""
Insert demo users, listings, lifestyle, tourism, and one pending booking.

Run from `backend/` after migrations:
  .\\.venv\\Scripts\\python scripts\\seed_demo.py

Requires DATABASE_URL in `.env`. Safe to re-run: skips if demo emails already exist.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))
load_dotenv(BACKEND / ".env")

from sqlalchemy import select  # noqa: E402

from app.core.database import SessionLocal  # noqa: E402
from app.models.booking import Booking  # noqa: E402
from app.models.enums import BookingStatus, ListingCategory, SleepCycle, UserRole  # noqa: E402
from app.models.listing import Listing  # noqa: E402
from app.models.lifestyle_profile import LifestyleProfile  # noqa: E402
from app.models.tourism_detail import TourismDetail  # noqa: E402
from app.models.user import User  # noqa: E402

DEMO_MARK = "seed.demo@urbanrelief.local"


def main() -> None:
    if SessionLocal is None:
        raise SystemExit("DATABASE_URL is not set (check backend/.env).")

    db = SessionLocal()
    try:
        existing = db.scalars(select(User).where(User.email == DEMO_MARK)).first()
        if existing is not None:
            print("Demo data already seeded (found user with demo marker email). Skipping.")
            return

        host_a = User(
            full_name="Demo Host A",
            phone="+8801700000001",
            email="host.a@urbanrelief.demo",
            role=UserRole.HOST,
            reputation_score=Decimal("4.85"),
        )
        host_b = User(
            full_name="Demo Host B (Female-only)",
            phone="+8801700000002",
            email="host.b@urbanrelief.demo",
            role=UserRole.HOST,
            reputation_score=Decimal("4.60"),
        )
        guest = User(
            full_name="Demo Guest",
            phone="+8801700000003",
            email=DEMO_MARK,
            role=UserRole.GUEST,
            reputation_score=Decimal("0"),
        )
        db.add_all([host_a, host_b, guest])
        db.flush()

        listings = [
            Listing(
                owner_id=host_a.id,
                title="Gulshan Short Stay",
                description="Quiet flat near Gulshan.",
                category=ListingCategory.SHORT_STAY,
                latitude=23.7925,
                longitude=90.4078,
                price_daily=Decimal("3500.00"),
                amenities={"wifi": True},
            ),
            Listing(
                owner_id=host_b.id,
                title="Bachelor Pad Dhanmondi",
                description="Shared bachelor; female-only host policy.",
                category=ListingCategory.BACHELOR,
                latitude=23.7461,
                longitude=90.3742,
                price_daily=Decimal("1200.00"),
                amenities={"female_only": True, "wifi": True},
            ),
            Listing(
                owner_id=host_a.id,
                title="Sylhet Tea Garden Homestay",
                description="Tourism homestay with local guide.",
                category=ListingCategory.TOURISM,
                latitude=24.8949,
                longitude=91.8687,
                price_daily=Decimal("2800.00"),
                amenities={"home_stay": True},
            ),
        ]
        db.add_all(listings)
        db.flush()

        db.add(
            TourismDetail(
                listing_id=listings[2].id,
                has_guide=True,
                local_food_available=True,
                adventure_gear_rental={"kayak": True, "life_jacket": True},
            )
        )

        db.add(
            LifestyleProfile(
                user_id=guest.id,
                is_smoker=False,
                job_type="remote",
                sleep_cycle=SleepCycle.NORMAL,
                cleanliness_score=8,
            )
        )

        db.add(
            Booking(
                user_id=guest.id,
                listing_id=listings[0].id,
                check_in=date.today(),
                check_out=date.today() + timedelta(days=2),
                total_amount=Decimal("7000.00"),
                status=BookingStatus.PENDING,
            )
        )

        db.commit()
        print("Demo seed OK.")
        print(f"  Guest user id (pass as VIEWER_USER_ID / Bachelor match): {guest.id}")
        print(f"  Listing ids: {[x.id for x in listings]}")
        print(f"  Pending booking for guest → listing {listings[0].id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
