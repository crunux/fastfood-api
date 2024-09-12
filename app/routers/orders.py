from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth import get_current_active_user
from app.controllers.orders import create_order
from app.database import get_session
from app.models.orders import OrderCreate, OrderInDB
from app.models.users import UserInDB

router = APIRouter(tags=["Orders"], responses={
                   404: {"description": "Not found"}})


@router.post("", response_model=OrderInDB)
def create_a_order(order: OrderCreate, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> OrderInDB:
    return create_order(order, userAccess, db)
