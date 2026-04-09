from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import NidStatus, UserRole


class UserBase(BaseModel):
    full_name: str = Field(..., max_length=255)
    phone: str = Field(..., max_length=32)
    email: EmailStr
    role: UserRole = UserRole.GUEST


class UserCreate(UserBase):
    reputation_score: Decimal | None = None
    nid_status: NidStatus | None = None


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=32)
    email: EmailStr | None = None
    role: UserRole | None = None
    nid_status: NidStatus | None = None
    reputation_score: Decimal | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nid_status: NidStatus
    reputation_score: Decimal
