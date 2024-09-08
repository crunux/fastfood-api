from fastapi import APIRouter, Depends
from app.database import get_session
from app.models.categories import Category, CategoryCreate, CategoryUpdate, CategoryInDB
from app.controllers import create_category, get_categories, get_category_by_id, update_category, delete_category
import uuid

router = APIRouter(tags=["Categories"], responses={
                   404: {"description": "Not found"}})


@router.post("", tags=["Categories"])
async def create_a_category(newCategory: CategoryCreate, db=Depends(get_session)):
    return create_category(newCategory, db)


@router.get("", tags=["Categories"], response_model=list[CategoryInDB])
async def read_categories(db=Depends(get_session)):
    return get_categories(db)


@router.get("/{category_id}", tags=["Categories"], response_model=CategoryInDB)
async def read_a_category(category_id: uuid.UUID, db=Depends(get_session)):
    return get_category_by_id(category_id, db)


@router.put("/{category_id}", tags=["Categories"], response_model=CategoryInDB)
async def update_a_category(category_id: uuid.UUID, updateCategory: CategoryUpdate, db=Depends(get_session)):
    return update_category(category_id, updateCategory, db)


@router.delete("/{category_id}", tags=["Categories"], response_model=dict)
async def delete_a_category(category_id: uuid.UUID, db=Depends(get_session)):
    return delete_category(category_id, db)
