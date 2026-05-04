from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from app.modules.users.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
    UserUpdate,
)
from app.modules.users.models import User
from app.modules.users.service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = UserService.create_user(db, user_data.dict())
    return user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = UserService.authenticate_user(db, login_data.email, login_data.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    print(f"Created token for user {user.id}: {access_token[:50]}...")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile"""
    user = UserService.update_user(
        db, current_user.id, update_data.dict(exclude_unset=True)
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user by ID (requires authentication)"""
    return UserService.get_user_by_id(db, user_id)
