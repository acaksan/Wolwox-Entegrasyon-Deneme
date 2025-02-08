import logging
from typing import Any, Dict

from fastapi import APIRouter
from src.services.firebird_service import FirebirdService
from src.services.woocommerce_service import WooCommerceService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get(
    "/connections",
    tags=["test"],
    response_model=Dict[str, Dict[str, Any]],
    description="Firebird ve WooCommerce bağlantılarını test eder",
    responses={
        200: {
            "description": "Başarılı yanıt",
            "content": {
                "application/json": {
                    "example": {
                        "firebird": {
                            "status": True,
                            "message": "Firebird bağlantısı başarılı"
                        },
                        "woocommerce": {
                            "status": True,
                            "message": "WooCommerce bağlantısı başarılı"
                        }
                    }
                }
            }
        }
    }
)
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
        logger.error(f"Firebird bağlantı hatası: {str(e)}")
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
        logger.error(f"WooCommerce bağlantı hatası: {str(e)}")
        results["woocommerce"]["message"] = str(e)

    return results