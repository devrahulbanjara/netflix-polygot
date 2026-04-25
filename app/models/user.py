from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)

class UserResponse(BaseModel):
    user_id: UUID
    email: str
    full_name: str
    created_at: datetime
    is_active: bool

class SubscriptionCreate(BaseModel):
    plan_name: str = Field(..., pattern="^(basic|standard|premium)$")