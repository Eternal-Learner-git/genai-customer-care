from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from models import UserRole, ComplaintStatus, ComplaintPriority


# ---------- User schemas ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Complaint schemas ----------

class ComplaintCreate(BaseModel):
    subject: str
    description: str


class ComplaintUpdate(BaseModel):
    status: Optional[ComplaintStatus] = None
    priority: Optional[ComplaintPriority] = None
    category: Optional[str] = None
    sentiment: Optional[str] = None
    suggested_response: Optional[str] = None


class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    description: str
    category: Optional[str]
    sentiment: Optional[str]
    priority: ComplaintPriority
    status: ComplaintStatus
    suggested_response: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: datetime
