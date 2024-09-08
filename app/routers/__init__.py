from fastapi import APIRouter, Depends
from app.auth import authent
from app.routers import products
from app.routers import users
from app.routers import categories

api = APIRouter()

api.include_router(products.router, prefix="/products",
                   tags=["Products"], dependencies=[Depends(authent)])
api.include_router(users.router, prefix="/users",
                   tags=["Users"], dependencies=[Depends(authent)])
api.include_router(categories.router, prefix="/categories",
                   tags=["Categories"], dependencies=[Depends(authent)])
