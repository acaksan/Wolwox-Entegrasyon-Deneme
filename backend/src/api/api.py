"""API router yapılandırması"""

import logging

from fastapi import APIRouter
from src.api.v1 import api_router as api_v1_router
from src.services.firebird_service import FirebirdService
from src.services.woocommerce_service import WooCommerceService

# Ana router
api_router = APIRouter()
logger = logging.getLogger(__name__)

# v1 API'sini /api/v1 prefix'i ile ekle
api_router.include_router(api_v1_router, prefix="/v1")

@api_router.get("/test/connections", tags=["test"])
async def test_connections():
    results = {
        "firebird": {"status": False, "message": ""},
        "woocommerce": {"status": False, "message": ""}
    }
    
    # Firebird Test
    try:
        fb_service = FirebirdService()
        await fb_service.test_connection()
        results["firebird"] = {
            "status": True,
            "message": "Firebird bağlantısı başarılı"
        }
    except Exception as e:
        logger.error(f"❌ Firebird bağlantı hatası: {str(e)}")
        results["firebird"]["message"] = str(e)

    # WooCommerce Test
    try:
        woo_service = WooCommerceService()
        await woo_service.test_connection()
        results["woocommerce"] = {
            "status": True,
            "message": "WooCommerce bağlantısı başarılı"
        }
    except Exception as e:
        logger.error(f"❌ WooCommerce bağlantı hatası: {str(e)}")
        results["woocommerce"]["message"] = str(e)

    return results

__all__ = ['api_router']
