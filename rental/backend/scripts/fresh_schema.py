"""
DESTRUCTIVE: Drop all ORM-defined tables and recreate from SQLAlchemy models.

Use only when you have no data to keep. Prefer Alembic (`alembic upgrade head`) for normal use.

Run from `backend/`:
  .\\.venv\\Scripts\\python scripts\\fresh_schema.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))
load_dotenv(BACKEND / ".env")

from sqlalchemy import create_engine  # noqa: E402

from app.core.database import Base  # noqa: E402
import app.models  # noqa: E402, F401


def main() -> None:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise SystemExit("DATABASE_URL is not set (check backend/.env).")

    engine = create_engine(url, pool_pre_ping=True)
    print("Dropping tables defined in Base.metadata...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables from models...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    main()
