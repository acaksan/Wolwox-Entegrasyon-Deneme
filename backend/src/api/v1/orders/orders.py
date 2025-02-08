"""Sipariş API endpoint'leri"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.utils.logger import logger
from src.wolvox.wolvox_service import WolvoxService


class OrderResponse(BaseModel):
    """Sipariş yanıt şeması"""
    siparis_no: str
    tarih: str
    musteri_kodu: str
    musteri_adi: str
    toplam_tutar: float
    durum: str

class OrderMeta(BaseModel):
    """Sayfalama meta bilgileri"""
    total: int
    page: int
    limit: int
    pages: int

class OrderList(BaseModel):
    """Sipariş listesi şeması"""
    data: List[OrderResponse]
    meta: OrderMeta

# Router'ı oluştur
router = APIRouter(prefix="/orders", tags=["orders"])

# Wolvox servisini başlat
wolvox_service = WolvoxService()

@router.get("/wolvox", response_model=OrderList)
async def get_wolvox_orders(
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    limit: int = Query(10, ge=1, le=100, description="Sayfa başına sipariş sayısı"),
    search: Optional[str] = Query(None, description="Arama terimi (sipariş no, müşteri kodu veya adı)")
):
    """
    Wolvox'tan siparişleri getir
    
    Args:
        page: Sayfa numarası
        limit: Sayfa başına sipariş sayısı
        search: Arama terimi
        
    Returns:
        OrderList: Sipariş listesi ve meta bilgiler
    """
    try:
        # Siparişleri getir
        orders = await wolvox_service.get_orders(
            page=page,
            limit=limit,
            search=search
        )
        
        # Toplam sipariş sayısını al
        total = await wolvox_service.get_order_count(search)
        
        return OrderList(
            data=orders,
            meta=OrderMeta(
                total=total,
                page=page,
                limit=limit,
                pages=(total + limit - 1) // limit
            )
        )
        
    except Exception as e:
        logger.error(f"Sipariş getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sipariş getirme hatası: {str(e)}"
        )

@router.get("/wolvox/{siparis_no}", response_model=OrderResponse)
async def get_wolvox_order(siparis_no: str):
    """
    Wolvox'tan tek sipariş getir
    
    Args:
        siparis_no: Sipariş numarası
        
    Returns:
        OrderResponse: Sipariş detayları
    """
    try:
        order = await wolvox_service.get_order(siparis_no)
        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Sipariş bulunamadı: {siparis_no}"
            )
        return OrderResponse(**order)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sipariş getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sipariş getirme hatası: {str(e)}"
        )

@router.get("/woocommerce")
async def get_wc_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """WooCommerce siparişlerini listele"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_orders(page=page, per_page=per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/woocommerce/{order_id}")
async def get_wc_order(order_id: int) -> Dict[str, Any]:
    """WooCommerce sipariş detayı getir"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sync/{order_id}")
async def sync_order(order_id: int) -> Dict[str, Any]:
    """WooCommerce'den Wolvox'a sipariş senkronizasyonu"""
    try:
        # WooCommerce'den sipariş bilgilerini al
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        wc_order = await wc_service.get_order(order_id)
        if not wc_order:
            raise HTTPException(status_code=404, detail="WooCommerce siparişi bulunamadı")

        # Wolvox'a aktar
        order = await wolvox_service.create_order({
            "musteri_kodu": wc_order["customer_id"],
            "musteri_adi": f"{wc_order['billing']['first_name']} {wc_order['billing']['last_name']}",
            "tutar": float(wc_order["total"]),
            "kdv": float(wc_order["total_tax"]),
            "toplam": float(wc_order["total"]) + float(wc_order["total_tax"]),
            "durum": wc_order["status"],
            "kalemler": [
                {
                    "stok_kodu": item["sku"],
                    "miktar": item["quantity"],
                    "fiyat": float(item["price"]),
                    "kdv_orani": float(item["total_tax"]) / float(item["total"]) * 100 if float(item["total"]) > 0 else 0
                }
                for item in wc_order["line_items"]
            ]
        })

        return {
            "wc_order": wc_order,
            "wolvox_order": order
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 