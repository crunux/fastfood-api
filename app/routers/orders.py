from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth import get_current_active_user
from app.controllers.orders import create_order, get_orders, get_order_by_id, update_order, delete_order
from app.database import get_session
from app.models.orders import OrderCreate, OrderInDB, OrderUpdate
from app.models.users import UserInDB

router = APIRouter(tags=["Orders"], responses={
                   404: {"description": "Not found"}})


@router.post("", response_model=OrderInDB)
def create_a_order(order: OrderCreate, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> OrderInDB:
    return create_order(order, userAccess, db)


@router.get("", response_model=list[OrderInDB])
def all_orders(userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> list[OrderInDB]:
    return get_orders(db)


@router.get("/{order_id}", response_model=OrderInDB)
def order_by_id(order_id: uuid.UUID, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> OrderInDB:
    return get_order_by_id(order_id, db)


@router.put("/{order_id}", response_model=OrderInDB)
def update(order_id: uuid.UUID, order: OrderUpdate, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> OrderInDB:
    return update_order(order_id, order, db)


@router.delete("/{order_id}", response_model=dict)
def delete(order_id: uuid.UUID, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> dict:
    return delete_order(order_id, db)
