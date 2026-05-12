from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class SubscriberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=80, examples=["Alice Khan"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    membership_type: str = Field(
        default="basic",
        pattern="^(basic|premium|student)$",
        description="Allowed values: basic, premium, student",
    )
    active: bool = Field(default=True)


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberReplace(SubscriberBase):
    pass


class SubscriberUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    email: Optional[EmailStr] = None
    membership_type: Optional[str] = Field(
        default=None,
        pattern="^(basic|premium|student)$",
    )
    active: Optional[bool] = None


class SubscriberOut(SubscriberBase):
    id: int
    photo_url: Optional[str] = None
