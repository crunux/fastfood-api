from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
import uuid
from app.config import settings
from app.database import get_session
from app.controllers.users import get_user_by_email, login
from app.models.users import UserInDB, LoginUser
from app.utils.generic_models import Msg, OAuth2CustomPasswordRequestForm, TokenResponse
from app.auth import create_token, get_current_user

router = APIRouter(responses={
                   404: {"description": "Not found"}})


@router.post("/token", response_model=TokenResponse)
async def login_user(login_user: Annotated[OAuth2CustomPasswordRequestForm, Depends(LoginUser)], db: Session = Depends(get_session)) -> TokenResponse:
    return login(login_user, db)


@router.get("/test-token", response_model=UserInDB)
async def get_current_user_data(user: UserInDB = Depends(get_current_user)) -> UserInDB:
    return user


@router.get("/password-recovery/{email}", response_model=Msg)
def reset_password(email: str, db: Annotated[Session, Depends(get_session)]):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The user with this username does not exist in the system.")
    password_reset_token = create_token(data={"sub": user.email}, expires_delta=timedelta(
        hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS))
    # send email with password recovery token
    return {"msg": "Password recovery email sent"}
