from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
from auth import create_access_token, verify_password, get_current_user, require_admin
from database import engine, get_db, Base

# Creates tables on startup if they don't exist yet.
# For a real production system you'd switch to Alembic migrations, but this is fine to start.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GenAI Customer Care API")

# Allow the React frontend (running on a different port) to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------- Auth endpoints ----------

@app.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)  # OAuth2 form uses "username" for the email field
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ---------- Complaint endpoints ----------

@app.post("/complaints", response_model=schemas.ComplaintOut, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint: schemas.ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_complaint(db, complaint, owner_id=current_user.id)


@app.get("/complaints/me", response_model=List[schemas.ComplaintOut])
def list_my_complaints(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_complaints_for_user(db, owner_id=current_user.id)


@app.get("/complaints", response_model=List[schemas.ComplaintOut])
def list_all_complaints(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    """Admin-only: view every complaint, for the admin dashboard."""
    return crud.get_all_complaints(db)


@app.get("/complaints/{complaint_id}", response_model=schemas.ComplaintOut)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    complaint = crud.get_complaint(db, complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if complaint.owner_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this complaint")
    return complaint


@app.patch("/complaints/{complaint_id}", response_model=schemas.ComplaintOut)
def update_complaint(
    complaint_id: int,
    updates: schemas.ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    """Admin-only for now: update status/priority/category, e.g. after AI classification or manual review."""
    updated = crud.update_complaint(db, complaint_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated


@app.delete("/complaints/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin),
):
    deleted = crud.delete_complaint(db, complaint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Complaint not found")
