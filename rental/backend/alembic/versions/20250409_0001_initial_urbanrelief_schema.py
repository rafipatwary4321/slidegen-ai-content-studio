"""initial urbanrelief schema

Revision ID: 20250409_0001
Revises:
Create Date: 2025-04-09

Creates users, listings, bookings, lifestyle_profiles, tourism_details.
Enum fields use VARCHAR (SQLAlchemy Enum native_enum=False).
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20250409_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="Guest"),
        sa.Column("nid_status", sa.String(length=32), nullable=False, server_default="Unverified"),
        sa.Column("reputation_score", sa.Numeric(precision=5, scale=2), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "listings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("price_daily", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("price_monthly", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("amenities", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_listings_owner_id"), "listings", ["owner_id"], unique=False)
    op.create_index(op.f("ix_listings_category"), "listings", ["category"], unique=False)

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("listing_id", sa.Integer(), nullable=False),
        sa.Column("check_in", sa.Date(), nullable=False),
        sa.Column("check_out", sa.Date(), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="Pending"),
        sa.Column("digital_key", sa.String(length=6), nullable=True),
        sa.Column("agreement_document_url", sa.String(length=2048), nullable=True),
        sa.ForeignKeyConstraint(["listing_id"], ["listings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("digital_key"),
    )
    op.create_index(op.f("ix_bookings_user_id"), "bookings", ["user_id"], unique=False)
    op.create_index(op.f("ix_bookings_listing_id"), "bookings", ["listing_id"], unique=False)

    op.create_table(
        "lifestyle_profiles",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_smoker", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("job_type", sa.String(length=128), nullable=True),
        sa.Column("sleep_cycle", sa.String(length=32), nullable=False),
        sa.Column("cleanliness_score", sa.SmallInteger(), nullable=False),
        sa.CheckConstraint(
            "cleanliness_score >= 1 AND cleanliness_score <= 10",
            name="ck_lifestyle_cleanliness_score",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )

    op.create_table(
        "tourism_details",
        sa.Column("listing_id", sa.Integer(), nullable=False),
        sa.Column("has_guide", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("local_food_available", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("adventure_gear_rental", postgresql.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["listing_id"], ["listings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("listing_id"),
    )


def downgrade() -> None:
    op.drop_table("tourism_details")
    op.drop_table("lifestyle_profiles")
    op.drop_table("bookings")
    op.drop_table("listings")
    op.drop_table("users")
