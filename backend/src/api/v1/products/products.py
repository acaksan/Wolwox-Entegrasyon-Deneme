"""Ürün API endpoint'leri"""

from typing import Any, Dict, List, Optional

from core.logging import logger
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.wolvox.wolvox_service import WolvoxService


class ProductResponse(BaseModel):
    """Ürün yanıt şeması"""
    stok_kodu: str
    stok_adi: str
    barkod: Optional[str] = None
    satis_fiyat1: float
    stok_miktari: float
    birim: str
    kdv_orani: float
    grup_kodu: Optional[str] = None
    marka_kodu: Optional[str] = None

class ProductMeta(BaseModel):
    """Sayfalama meta bilgileri"""
    total: int
    page: int
    limit: int
    pages: int

class ProductList(BaseModel):
    """Ürün listesi şeması"""
    data: List[ProductResponse]
    meta: ProductMeta

# Router'ı oluştur
router = APIRouter(prefix="/products", tags=["products"])

# Wolvox servisini başlat
wolvox_service = WolvoxService()

@router.get("/wolvox", response_model=ProductList)
async def get_wolvox_products(
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    limit: int = Query(10, ge=1, le=100, description="Sayfa başına ürün sayısı"),
    search: Optional[str] = Query(None, description="Arama terimi (stok kodu, ad veya barkod)")
):
    """Test verileri döndür"""
    # Test verileri
    test_products = [
        {
            "stok_kodu": "TEST001",
            "stok_adi": "Test Ürün 1",
            "barkod": "1234567890",
            "satis_fiyat1": 100.0,
            "stok_miktari": 50.0,
            "birim": "ADET",
            "kdv_orani": 18.0,
            "grup_kodu": "G1",
            "marka_kodu": "M1"
        },
        {
            "stok_kodu": "TEST002",
            "stok_adi": "Test Ürün 2",
            "barkod": "0987654321",
            "satis_fiyat1": 200.0,
            "stok_miktari": 30.0,
            "birim": "ADET",
            "kdv_orani": 18.0,
            "grup_kodu": "G1",
            "marka_kodu": "M2"
        }
    ]
    
    total = len(test_products)
    pages = (total + limit - 1) // limit
    
    return ProductList(
        data=test_products,
        meta=ProductMeta(
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
    )

@router.get("/wolvox/{stok_kodu}", response_model=ProductResponse)
async def get_wolvox_product(stok_kodu: str):
    """
    Wolvox'tan tek ürün getir
    
    Args:
        stok_kodu: Ürün stok kodu
        
    Returns:
        ProductResponse: Ürün detayları
    """
    try:
        # Test verileri
        test_products = [
            {
                "stok_kodu": "TEST001",
                "stok_adi": "Test Ürün 1",
                "barkod": "1234567890",
                "satis_fiyat1": 100.0,
                "stok_miktari": 50.0,
                "birim": "ADET",
                "kdv_orani": 18.0,
                "grup_kodu": "G1",
                "marka_kodu": "M1"
            },
            {
                "stok_kodu": "TEST002",
                "stok_adi": "Test Ürün 2",
                "barkod": "0987654321",
                "satis_fiyat1": 200.0,
                "stok_miktari": 30.0,
                "birim": "ADET",
                "kdv_orani": 18.0,
                "grup_kodu": "G1",
                "marka_kodu": "M2"
            }
        ]
        
        product = next((product for product in test_products if product["stok_kodu"] == stok_kodu), None)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Ürün bulunamadı: {stok_kodu}"
            )
        return ProductResponse(**product)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ürün getirme hatası: {str(e)}"
        )

@router.get("/woocommerce")
async def get_wc_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """WooCommerce ürünlerini listele"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_products(page=page, per_page=per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/woocommerce/{product_id}")
async def get_wc_product(product_id: int) -> Dict[str, Any]:
    """WooCommerce ürün detayı getir"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sync/{product_code}")
async def sync_product(product_code: str) -> Dict[str, Any]:
    """Wolvox'tan WooCommerce'e ürün senkronizasyonu"""
    try:
        # Wolvox'tan ürün bilgilerini al
        # Test verileri
        test_products = [
            {
                "stok_kodu": "TEST001",
                "stok_adi": "Test Ürün 1",
                "barkod": "1234567890",
                "satis_fiyat1": 100.0,
                "stok_miktari": 50.0,
                "birim": "ADET",
                "kdv_orani": 18.0,
                "grup_kodu": "G1",
                "marka_kodu": "M1"
            },
            {
                "stok_kodu": "TEST002",
                "stok_adi": "Test Ürün 2",
                "barkod": "0987654321",
                "satis_fiyat1": 200.0,
                "stok_miktari": 30.0,
                "birim": "ADET",
                "kdv_orani": 18.0,
                "grup_kodu": "G1",
                "marka_kodu": "M2"
            }
        ]
        
        wolvox_product = next((product for product in test_products if product["stok_kodu"] == product_code), None)
        if not wolvox_product:
            raise HTTPException(status_code=404, detail="Wolvox ürünü bulunamadı")

        # WooCommerce'de güncelle/oluştur
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        wc_product = await wc_service.update_product(
            product_id=wolvox_product.get("wc_product_id"),  # Eğer varsa
            data={
                "name": wolvox_product["stok_adi"],
                "regular_price": str(wolvox_product["satis_fiyat1"]),
                "sku": wolvox_product["stok_kodu"],
                "manage_stock": True,
                "stock_quantity": wolvox_product.get("stok_miktari", 0)
            }
        )

        return {
            "wolvox_product": wolvox_product,
            "wc_product": wc_product
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 