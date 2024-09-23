from decimal import Decimal
from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlmodel import Session
import uuid
from app.auth import get_current_active_admin, get_current_active_user
from app.database import get_session
from app.models.products import ProductCreate, ProductInDB, ProductUpdate
from app.controllers import create_product, get_products, get_product_by_id, update_product, delete_product
from app.models.users import UserInDB


router = APIRouter(responses={
                   404: {"description": "Not found"}})


# async def create_a_product(newProduct: ProductCreate, userAccess: Annotated[UserInDB,  Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> ProductInDB:
@router.post("", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_a_product(name: Annotated[str, Form()], description: Annotated[str, Form()], price: Annotated[Decimal, Form()], category_id: Annotated[uuid.UUID, Form()], image: Annotated[UploadFile, File()], userAccess: Annotated[UserInDB,  Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> ProductInDB:
    print(image, "imagen router")
    product = ProductCreate(name=name, description=description, price=price, category_id=category_id, active=True)
    return await create_product(product, image, db)


@router.get("", response_model=list[ProductInDB])
async def read_products(userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> list[ProductInDB]:
    return get_products(userAccess, db)


@router.get("/{product_id}", response_model=ProductInDB)
async def read_a_product(product_id: uuid.UUID, userAccess: Annotated[UserInDB, Depends(get_current_active_user)], db: Session = Depends(get_session)) -> ProductInDB:
    return get_product_by_id(product_id, db)


@router.put("/{product_id}", response_model=ProductInDB)
async def update_a_product(product_id: uuid.UUID, product: ProductUpdate, userAccess: Annotated[UserInDB, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> ProductInDB:
    return update_product(product_id, product, db)


@router.delete("/{product_id}", response_model=dict)
async def delete_a_product(product_id: uuid.UUID, userAccess: Annotated[UserInDB, Depends(get_current_active_admin)], db: Session = Depends(get_session)) -> dict:
    return delete_product(product_id, db)
