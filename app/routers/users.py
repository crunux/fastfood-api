from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid
from app.auth import get_current_active_admin
from app.controllers.users import create, get_users, get_user_by_id, update, delete, login
from app.database import get_session
from app.models.users import User, UserInDB, UserCreate, UserUpdate

router = APIRouter(tags=["Users"], responses={
                   404: {"description": "Not found"}})


@router.post("", response_model=UserInDB)
async def create_user(user: UserCreate, userAccess: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> UserInDB:
    print(user)
    return create(user, userAccess, db)


@router.get("", response_model=list[UserInDB])
async def get_users_list(userAccess: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> list[UserInDB]:
    return get_users(userAccess, db)


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, userAccess: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> UserInDB:
    return get_user_by_id(user_id, userAccess, db)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: uuid.UUID, user: UserUpdate, userAccess: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> UserInDB:
    return update(user_id, user, userAccess, db)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: uuid.UUID, userAccess: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> dict:
    return delete(user_id, userAccess, db)
