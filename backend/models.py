import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UserRole(str, enum.Enum):
    customer = "customer"
    admin = "admin"


class ComplaintStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class ComplaintPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="owner")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # Filled in later by the NLP engine; nullable so the row can exist before classification runs
    category = Column(String(100), nullable=True)
    sentiment = Column(String(50), nullable=True)
    priority = Column(Enum(ComplaintPriority), default=ComplaintPriority.medium, nullable=False)

    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.open, nullable=False)

    # Filled in later by the RAG/LLM engine
    suggested_response = Column(Text, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="complaints")
