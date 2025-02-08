# Sipariş entegrasyonu

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.order import Order, OrderCreate, OrderResponse, OrderUpdate
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.utils.cache import cache_manager
from src.utils.logger import log_event
from src.wolvox.wolvox_service import WolvoxService

router = APIRouter()
wolvox_service = WolvoxService()

@router.get("/", response_model=List[Order])
async def list_orders(db: Session = Depends(get_db)):
    """Tüm siparişleri listele"""
    try:
        orders = wolvox_service.get_orders()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """Belirli bir siparişi getir"""
    try:
        order = wolvox_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync")
async def sync_orders(db: Session = Depends(get_db)):
    """WooCommerce'den yeni siparişleri al ve Wolvox'a aktar"""
    try:
        result = wolvox_service.sync_orders()
        return {"message": "Sipariş senkronizasyonu başarılı", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: str,
    order: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Sipariş durumunu güncelle"""
    try:
        updated_order = wolvox_service.update_order(order_id, order)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Yeni sipariş oluştur."""
    try:
        new_order = wolvox_service.create_order(db, order)
        # Cache'i temizle
        await cache_manager.delete_pattern("orders_list_*")
        
        log_event("INFO", "orders", f"Yeni sipariş oluşturuldu: {new_order.id}")
        return new_order
    except Exception as e:
        log_event("ERROR", "orders", "Sipariş oluşturulamadı", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sipariş oluşturulurken bir hata oluştu"
        )

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Sipariş sil."""
    try:
        result = wolvox_service.delete_order(db, order_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sipariş bulunamadı"
            )

        # Cache'i temizle
        await cache_manager.delete(f"order_{order_id}")
        await cache_manager.delete_pattern("orders_list_*")
        
        log_event("INFO", "orders", f"Sipariş silindi: {order_id}")
    except HTTPException:
        raise
    except Exception as e:
        log_event("ERROR", "orders", f"Sipariş silinemedi: {order_id}", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sipariş silinirken bir hata oluştu"
        )
