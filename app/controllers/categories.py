from sqlmodel import Session, select
from fastapi import status, Depends, HTTPException
import uuid
from app.models.categories import Category, CategoryCreate, CategoryInDB, CategoryUpdate
from app.database import get_session


def create_category(category: CategoryCreate, db: Session = Depends(get_session)) -> CategoryInDB:
    category = Category.model_validate(category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session = Depends(get_session)) -> list[CategoryInDB]:
    statement = select(Category).order_by(Category.id)
    categories = db.exec(statement).all()
    return categories


def get_category_by_id(id: uuid.UUID, db: Session = Depends(get_session)) -> CategoryInDB:
    statement = select(Category).where(Category.id == id)
    category = db.exec(statement).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found with id: {id}")
    return category


def update_category(id: uuid.UUID, category: CategoryUpdate, db: Session = Depends(get_session)) -> CategoryInDB:
    category_update = db.get(Category, id)
    if not category_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found with id: {id}")
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(category_update, key, value)

    db.add(category)
    db.commit()
    db.refresh(category)
    return get_category_by_id(id, db)


def delete_category(id: uuid.UUID, db: Session = Depends(get_session)) -> dict:
    category = db.get(Category, id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found with id: {id}")

    db.delete(category)
    db.commit()
    return {"deleted": True, "message": f"Category {id} deleted"}
