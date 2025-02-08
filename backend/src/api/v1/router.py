"""API router'ı"""

from api.v1.customers.customers import router as customers_router
from api.v1.health import router as health_router
from api.v1.orders.orders import router as orders_router
from api.v1.products.products import router as products_router
from api.v1.sync import router as sync_router
from fastapi import APIRouter

# Ana router
api_router = APIRouter()

# Alt routerları ekle
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(products_router, tags=["products"])
api_router.include_router(orders_router, tags=["orders"])
api_router.include_router(customers_router, tags=["customers"])
api_router.include_router(sync_router, prefix="/sync", tags=["sync"])