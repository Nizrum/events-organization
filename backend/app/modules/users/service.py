from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        # Check if user exists
        existing_user = (
            db.query(User).filter(User.email == user_data["email"]).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash password
        hashed_password = get_password_hash(user_data["password"])

        # Create user
        db_user = User(
            email=user_data["email"],
            hashed_password=hashed_password,
            name=user_data["name"],
            role=user_data["role"],
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict) -> User:
        user = UserService.get_user_by_id(db, user_id)

        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
