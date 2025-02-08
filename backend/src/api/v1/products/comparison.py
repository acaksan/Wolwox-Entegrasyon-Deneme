import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from src.models.wolvox.product import WlxProduct
from src.models.woocommerce.product import WooProduct
from src.repositories.wolvox.product_repository import WolvoxProductRepository
from src.repositories.woocommerce.product_repository import \
    WooCommerceProductRepository

router = APIRouter(prefix="/products", tags=["products"])
logger = logging.getLogger(__name__)

class ProductComparison(BaseModel):
    """Ürün karşılaştırma sonuç modeli"""
    matched_count: int
    matched_wolvox: List[WlxProduct]
    matched_woo: List[WooProduct]
    unmatched_wolvox: List[WlxProduct]
    unmatched_woo: List[WooProduct]

@router.get(
    "/comparison",
    response_model=ProductComparison,
    status_code=status.HTTP_200_OK,
)
async def compare_products(
    match_by: str = Query("sku", description="Eşleştirme kriteri (sku, name)")
):
    """Wolvox ve WooCommerce ürünlerini karşılaştırır"""
    try:
        # Repository'leri başlat
        wolvox_repo = WolvoxProductRepository()
        woo_repo = WooCommerceProductRepository()
        
        # Ürünleri getir
        wolvox_products = await wolvox_repo.get_products()
        woo_products = await woo_repo.get_products()
        
        # Eşleştirme için dictionary'ler
        wolvox_dict = {
            getattr(p, match_by): p for p in wolvox_products if getattr(p, match_by)
        }
        woo_dict = {
            getattr(p, match_by): p for p in woo_products if getattr(p, match_by)
        }
        
        # Eşleşen ve eşleşmeyen ürünleri bul
        matched_wolvox = []
        matched_woo = []
        unmatched_wolvox = []
        unmatched_woo = []
        
        # Wolvox ürünlerini kontrol et
        for key, wolvox_product in wolvox_dict.items():
            if key in woo_dict:
                matched_wolvox.append(wolvox_product)
                matched_woo.append(woo_dict[key])
            else:
                unmatched_wolvox.append(wolvox_product)
        
        # WooCommerce'da olup Wolvox'ta olmayan ürünleri bul
        for key, woo_product in woo_dict.items():
            if key not in wolvox_dict:
                unmatched_woo.append(woo_product)
        
        return ProductComparison(
            matched_count=len(matched_wolvox),
            matched_wolvox=matched_wolvox,
            matched_woo=matched_woo,
            unmatched_wolvox=unmatched_wolvox,
            unmatched_woo=unmatched_woo
        )
        
    except Exception as e:
        logger.error(f"Ürün karşılaştırma hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 