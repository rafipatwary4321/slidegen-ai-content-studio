"""add tourism service fields to listings

Revision ID: 20260409_0002
Revises: 20250409_0001
Create Date: 2026-04-09
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op  # pylint: disable=import-error
from sqlalchemy.dialects import postgresql

revision: str = "20260409_0002"
down_revision: Union[str, None] = "20250409_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "listings",
        sa.Column(
            "has_guide",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "listings",
        sa.Column("guide_price", sa.Numeric(precision=12, scale=2), nullable=True),
    )
    op.add_column(
        "listings",
        sa.Column("available_gear", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.alter_column("listings", "has_guide", server_default=None)


def downgrade() -> None:
    op.drop_column("listings", "available_gear")
    op.drop_column("listings", "guide_price")
    op.drop_column("listings", "has_guide")

