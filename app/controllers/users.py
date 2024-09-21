from datetime import timedelta
import uuid
from sqlmodel import Session, select
from fastapi import status, HTTPException
from app.auth import create_token
from app.utils.security import hash_password, verify_password
from app.utils.generic_models import TokenResponse, OAuth2CustomPasswordRequestForm
from app.models.users import User, UserCreate, UserUpdate, UserInDB
from app.config import settings


def create(user: UserCreate, userAccess: User, db: Session) -> UserInDB:
    user_found = db.exec(select(User).where(User.email == user.email)).first()
    if user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {user.email} already exists")
    hashed_password = hash_password(user.password)
    extra_data = {"password_hash": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(login_user: OAuth2CustomPasswordRequestForm, db: Session) -> TokenResponse:
    user = get_user_by_email(login_user.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect email or password")
    if not verify_password(login_user.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer", "user": user}


def get_users(userAccess: UserInDB, db: Session) -> list[UserInDB]:
    statement = select(User).order_by(User.id)
    users = db.exec(statement).all()
    return users


def get_user_by_id(id: uuid.UUID, userAccess: UserInDB, db: Session) -> UserInDB:
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")
    return user


def get_user_by_email(email: str, db: Session) -> UserInDB:
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")
    return user


def update(id: uuid.UUID, user: UserUpdate, userAccess: UserInDB, db: Session) -> UserInDB:
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")
    user_data = user.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        hashed_password = hash_password(user_data["password"])
        extra_data["password_hash"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(id: uuid.UUID, userAccess: UserInDB, db: Session) -> dict:
    db_user = db.get(User, id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found with id: {id}")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully", "delete": True}
