import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from src.services.woocommerce_service import WooCommerceService

router = APIRouter(prefix="/woocommerce", tags=["woocommerce"])
logger = logging.getLogger(__name__)

@router.get(
    "/products/test",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def test_products():
    """WooCommerce'dan ham ürün verisini getirir"""
    try:
        woo_service = WooCommerceService()
        
        # İlk 5 ürünü getir
        response = woo_service.get("products", params={"per_page": 5})
        
        if not isinstance(response, list):
            logger.error(f"Beklenmeyen yanıt türü: {type(response)}")
            return []
            
        return response
        
    except Exception as e:
        logger.error(f"WooCommerce test hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 