from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.security import hash_password

from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.dependencies import get_db
from app.core.auth import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

# ---- POST: Create user ----
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
    name=user.name,
    email=user.email,
    hashed_password=hash_password(user.password)
)


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ---- GET: List users ----
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user
