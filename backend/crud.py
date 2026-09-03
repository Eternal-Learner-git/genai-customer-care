from sqlalchemy.orm import Session, joinedload

import models
import schemas
from auth import hash_password


# ---------- User CRUD ----------

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- Complaint CRUD ----------

def create_complaint(db: Session, complaint: schemas.ComplaintCreate, owner_id: int) -> models.Complaint:
    db_complaint = models.Complaint(
        subject=complaint.subject,
        description=complaint.description,
        owner_id=owner_id,
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def get_complaint(db: Session, complaint_id: int) -> models.Complaint | None:
    return (
        db.query(models.Complaint)
        .options(joinedload(models.Complaint.owner))
        .filter(models.Complaint.id == complaint_id)
        .first()
    )


def get_complaints_for_user(db: Session, owner_id: int, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Complaint)
        .options(joinedload(models.Complaint.owner))
        .filter(models.Complaint.owner_id == owner_id)
        .order_by(models.Complaint.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_complaints(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.Complaint)
        .options(joinedload(models.Complaint.owner))
        .order_by(models.Complaint.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_complaint(db: Session, complaint_id: int, updates: schemas.ComplaintUpdate) -> models.Complaint | None:
    db_complaint = get_complaint(db, complaint_id)
    if db_complaint is None:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_complaint, field, value)

    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def delete_complaint(db: Session, complaint_id: int) -> bool:
    db_complaint = get_complaint(db, complaint_id)
    if db_complaint is None:
        return False
    db.delete(db_complaint)
    db.commit()
    return True
