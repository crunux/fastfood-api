import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
from typing import Annotated
from pydantic import ValidationError

from app.database import get_session
from app.utils.generic_models import TokenData
from app.config import settings
from app.models.users import User


# basic_auth = HTTPBasic(auto_error=False)


ALGORITHM = "HS256"


bearer_auth = HTTPBearer(auto_error=False)


# def authent(credentials: HTTPBasicCredentials = Depends(basic_auth)):
#     return True
#     # if check_auth_creds(credentials):
#     #     return True
#     # raise HTTPException(
#     #     status_code=status.HTTP_401_UNAUTHORIZED,
#     #     detail="Incorrect user or password",
#     #     headers={"WWW-Authenticate": "Basic"},
#     # )


# def check_auth_creds(credentials: HTTPBasicCredentials = Depends(basic_auth)):
#     correct_username = secrets.compare_digest(
#         credentials.username, settings.API_USERNAME)
#     correct_password = secrets.compare_digest(
#         credentials.password, settings.API_PASSWORD)

#     if correct_username and correct_password:
#         return True

#     return False


def get_authorization_header(bearer: HTTPAuthorizationCredentials = Depends(bearer_auth)) -> str:
    if not bearer or bearer.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={
            "WWW-Authenticate": "Bearer"},)
    if bearer and bearer.credentials:
        return bearer.credentials
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(get_authorization_header)], db: Session = Depends(get_session)) -> dict:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={
                                          "WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    user = db.exec(select(User).where(User.email == token_data.email)).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[User, Security(get_current_user)],):
    if current_user.is_active:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")


def get_current_active_admin(current_user: Annotated[User, Security(get_current_user)],):
    if current_user.is_admin:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="The user doesn't have enough privileges")
