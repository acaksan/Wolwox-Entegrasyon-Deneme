# WooCommerce entegrasyonu

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas.product import (Product, ProductCreate, ProductResponse,
                             ProductUpdate)
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.utils.cache import cache_manager, get_cache
from src.utils.logger import log_error, log_event, log_info
from src.utils.metrics import track_sync_duration
from src.wolvox.wolvox_service import WolvoxService
from src.wolvox.woocommerce_service import WooCommerceService

router = APIRouter()
wolvox_service = WolvoxService()
cache = get_cache()

@router.get("/", response_model=List[Product])
async def list_products(db: Session = Depends(get_db)):
    """Tüm ürünleri listele"""
    try:
        products = wolvox_service.get_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Belirli bir ürünü getir"""
    try:
        product = wolvox_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sync")
@track_sync_duration
async def sync_products(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> dict:
    """Wolvox'tan WooCommerce'e ürün senkronizasyonu"""
    try:
        # Cache kontrolü
        cache_key = f"sync_products_{limit}_{offset}"
        cached_data = cache.get(cache_key)
        if cached_data:
            log_info("Cache'den veri alındı", "products_api")
            return cached_data

        # Wolvox'tan ürünleri al
        products = wolvox_service.get_products(limit, offset)
        
        # WooCommerce'e gönder
        woo = WooCommerceService()
        sync_results = woo.sync_products(products)
        
        # Sonuçları cache'le
        cache.set(cache_key, sync_results, expire=300)
        
        log_info(
            f"{len(products)} ürün senkronize edildi",
            "products_api",
            {"sync_results": sync_results}
        )
        return sync_results

    except Exception as e:
        log_error(e, "products_api", {
            "limit": limit,
            "offset": offset
        })
        raise HTTPException(
            status_code=500,
            detail="Ürün senkronizasyonu sırasında hata oluştu"
        )

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Ürün bilgilerini güncelle"""
    try:
        updated_product = wolvox_service.update_product(product_id, product)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Yeni ürün oluştur."""
    try:
        new_product = wolvox_service.create_product(db, product)
        # Cache'i temizle
        await cache_manager.delete_pattern("products_list_*")
        
        log_event("INFO", "products", f"Yeni ürün oluşturuldu: {new_product.id}")
        return new_product
    except Exception as e:
        log_event("ERROR", "products", "Ürün oluşturulamadı", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ürün oluşturulurken bir hata oluştu"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Ürün sil."""
    try:
        result = wolvox_service.delete_product(db, product_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ürün bulunamadı"
            )

        # Cache'i temizle
        await cache_manager.delete(f"product_{product_id}")
        await cache_manager.delete_pattern("products_list_*")
        
        log_event("INFO", "products", f"Ürün silindi: {product_id}")
    except HTTPException:
        raise
    except Exception as e:
        log_event("ERROR", "products", f"Ürün silinemedi: {product_id}", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ürün silinirken bir hata oluştu"
        )
