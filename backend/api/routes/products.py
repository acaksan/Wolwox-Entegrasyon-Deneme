"""Ürün rotaları.

Bu modül, ürünlerle ilgili API endpoint'lerini içerir.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from models.schemas import Product
from services.woocommerce_service import WooCommerceService
from services.wolvox_product_service import WolvoxProductService
from core.logging import logger
from exceptions.service_exception import ServiceException
from fastapi.responses import JSONResponse


router = APIRouter(tags=["Products"])
wolvox_product_service = WolvoxProductService()


@router.get("/products")
async def get_products() -> Dict[str, Any]:
    """WooCommerce'dan ürünleri getir.
    
    Returns:
        Dict[str, Any]: Ürün listesi ve durum bilgisi
        
    Raises:
        HTTPException: İstek sırasında oluşan hatalar
    """
    try:
        # WooCommerce'dan ürünleri çek
        woo_service = WooCommerceService()
        products = await woo_service.get_products()
        return {"status": "success", "data": products}
    except Exception as e:
        logger.error(f"Ürünler alınırken hata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products/sync", status_code=202)
async def sync_products() -> Dict[str, Any]:
    """Ürün senkronizasyonunu başlat.
    
    Returns:
        Dict[str, Any]: Senkronizasyon durumu ve sonuç
        
    Raises:
        HTTPException: Senkronizasyon sırasında oluşan hatalar
    """
    try:
        # Senkronizasyon işlemini başlat
        woo_service = WooCommerceService()
        result = await woo_service.sync_products()
        return {
            "status": "success",
            "message": "Senkronizasyon başlatıldı",
            "data": result
        }
    except Exception as e:
        logger.error(f"Senkronizasyon hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/products", status_code=201)
async def create_product(product: Product) -> Dict[str, Any]:
    """Yeni ürün oluştur.
    
    Args:
        product (Product): Oluşturulacak ürün bilgileri
        
    Returns:
        Dict[str, Any]: Oluşturulan ürün bilgileri ve durum
        
    Raises:
        HTTPException: Ürün oluşturma sırasında oluşan hatalar
    """
    try:
        # Ürün oluştur
        woo_service = WooCommerceService()
        result = await woo_service.create_product(product)
        return {
            "status": "success",
            "message": "Ürün başarıyla oluşturuldu",
            "data": result
        }
    except ServiceException as e:
        logger.error(f"Ürün oluşturma hatası: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": "Sunucu hatası oluştu. Lütfen daha sonra tekrar deneyin."
            }
        )


@router.get("/wolvox/products")
async def get_wolvox_products() -> Dict[str, Any]:
    """Wolvox'tan ürünleri getir.
    
    Returns:
        Dict[str, Any]: Ürün listesi
        
    Raises:
        HTTPException: İstek sırasında oluşan hatalar
    """
    try:
        products = await wolvox_product_service.get_products()
        return {"products": products}
    except Exception as e:
        logger.error(f"Wolvox ürünleri alınırken hata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 