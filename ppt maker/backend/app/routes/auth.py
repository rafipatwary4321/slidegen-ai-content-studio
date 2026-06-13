from fastapi import APIRouter, HTTPException, status

from app.models.schemas import AuthResponse, SignInRequest, SignUpRequest
from app.services.persistence import store

router = APIRouter()


@router.post("/auth/signup", response_model=AuthResponse)
def sign_up(payload: SignUpRequest) -> AuthResponse:
    user = store.sign_up_user(payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create account. Email may already be in use.",
        )
    return AuthResponse(success=True, message="Account created.", user=user)


@router.post("/auth/signin", response_model=AuthResponse)
def sign_in(payload: SignInRequest) -> AuthResponse:
    user = store.authenticate_user(payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return AuthResponse(success=True, message="Signed in.", user=user)
