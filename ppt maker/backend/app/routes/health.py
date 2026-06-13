from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "slidegen-ai-backend",
        "message": "Backend is healthy.",
    }
