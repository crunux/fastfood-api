from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
import uuid
from app.controllers.users import create, get_users, get_user_by_id, update, delete, login
from app.database import get_session
from app.models.users import UserInDB, UserCreate, UserUpdate, LoginUser
from app.utils.generic_models import OAuth2CustomPasswordRequestForm, TokenResponse

router = APIRouter(tags=["Users"], responses={
                   404: {"description": "Not found"}})


@router.post("", response_model=UserInDB)
async def create_user(user: UserCreate, db: Session = Depends(get_session)) -> UserInDB:
    print(user)
    return create(user, db)


@router.post("/login", response_model=TokenResponse)
async def login_user(login_user: Annotated[OAuth2CustomPasswordRequestForm, Depends(LoginUser)], db: Session = Depends(get_session)) -> TokenResponse:
    return login(login_user, db)


@router.get("", response_model=list[UserInDB])
async def get_users_list(db: Session = Depends(get_session)) -> list[UserInDB]:
    return get_users(db)


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, db: Session = Depends(get_session)) -> UserInDB:
    return get_user_by_id(user_id, db)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: uuid.UUID, user: UserUpdate, db: Session = Depends(get_session)) -> UserInDB:
    return update(user_id, user, db)


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: uuid.UUID, db: Session = Depends(get_session)) -> dict:
    return delete(user_id, db)
