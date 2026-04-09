from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _engine():
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
    )


engine = None
SessionLocal = None

if settings.database_url:
    engine = _engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("Database is not configured (DATABASE_URL empty)")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
