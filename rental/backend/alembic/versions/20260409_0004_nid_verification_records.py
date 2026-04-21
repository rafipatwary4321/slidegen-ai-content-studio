"""add nid verification records table

Revision ID: 20260409_0004
Revises: 20260409_0003
Create Date: 2026-04-09
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op  # pylint: disable=import-error

revision: str = "20260409_0004"
down_revision: Union[str, None] = "20260409_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "nid_verifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("image_path", sa.String(length=2048), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="Pending"),
        sa.Column("webhook_response", sa.Text(), nullable=True),
        sa.Column("webhook_error", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_nid_verifications_user_id"), "nid_verifications", ["user_id"], unique=False)
    op.alter_column("nid_verifications", "status", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_nid_verifications_user_id"), table_name="nid_verifications")
    op.drop_table("nid_verifications")

