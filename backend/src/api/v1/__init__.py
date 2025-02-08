"""API v1 paketi"""

from fastapi import APIRouter

from .customers import customers_router
from .orders import orders_router
from .products import products_router

# Ana router
router = APIRouter(prefix="/api/v1")

# Alt routerları ekle
router.include_router(products_router)
router.include_router(orders_router)
router.include_router(customers_router)

__all__ = ['router']
