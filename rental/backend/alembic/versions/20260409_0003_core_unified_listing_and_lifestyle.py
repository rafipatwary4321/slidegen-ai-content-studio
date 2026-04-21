"""core unified listing + listing lifestyle profile

Revision ID: 20260409_0003
Revises: 20260409_0002
Create Date: 2026-04-09
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op  # pylint: disable=import-error
from sqlalchemy.dialects import postgresql

revision: str = "20260409_0003"
down_revision: Union[str, None] = "20260409_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "listing_lifestyle_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("is_smoker", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("job_type", sa.String(length=128), nullable=True),
        sa.Column("sleep_cycle", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("listings", sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column("listings", sa.Column("lifestyle_profile_id", sa.Integer(), nullable=True))
    op.add_column(
        "listings",
        sa.Column("gear_available", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.create_index(
        op.f("ix_listings_lifestyle_profile_id"),
        "listings",
        ["lifestyle_profile_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_listings_lifestyle_profile_id_listing_lifestyle_profiles",
        "listings",
        "listing_lifestyle_profiles",
        ["lifestyle_profile_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_listings_lifestyle_profile_id_listing_lifestyle_profiles",
        "listings",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_listings_lifestyle_profile_id"), table_name="listings")
    op.drop_column("listings", "gear_available")
    op.drop_column("listings", "lifestyle_profile_id")
    op.drop_column("listings", "price")
    op.drop_table("listing_lifestyle_profiles")

