from fastapi import APIRouter
from app.routers import orders, products
from app.routers import users
from app.routers import categories
from app.routers import login

api = APIRouter()

api.include_router(products.router, prefix="/products",
                   tags=["Products"])

api.include_router(users.router, prefix="/users",
                   tags=["Users"])

api.include_router(login.router, prefix="/login",
                   tags=["Login"])

api.include_router(categories.router, prefix="/categories",
                   tags=["Categories"])

api.include_router(orders.router, prefix="/orders", tags=["Orders"])
