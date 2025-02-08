from fastapi import APIRouter
from src.api.v1 import orders, products, stock

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(stock.router, prefix="/stock", tags=["stock"]) 