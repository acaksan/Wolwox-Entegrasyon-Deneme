from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from schemas.stock import StockCheck, StockUpdate
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.wolvox.wolvox_service import WolvoxService

router = APIRouter()
wolvox_service = WolvoxService()

@router.get("/check", response_model=List[StockCheck])
async def check_stock(db: Session = Depends(get_db)):
    """Tüm ürünlerin stok durumunu kontrol et"""
    try:
        stock_status = wolvox_service.check_stock()
        return stock_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync")
async def sync_stock(db: Session = Depends(get_db)):
    """Wolvox ve WooCommerce arasında stok senkronizasyonu yap"""
    try:
        result = wolvox_service.sync_stock()
        return {"message": "Stok senkronizasyonu başarılı", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}")
async def update_stock(
    product_id: str,
    stock: StockUpdate,
    db: Session = Depends(get_db)
):
    """Ürün stok miktarını güncelle"""
    try:
        result = wolvox_service.update_stock(product_id, stock.quantity)
        if not result:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return {"message": "Stok güncellendi", "product_id": product_id, "quantity": stock.quantity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/low", response_model=List[StockCheck])
async def get_low_stock(db: Session = Depends(get_db)):
    """Düşük stoklu ürünleri listele"""
    try:
        low_stock = wolvox_service.get_low_stock()
        return low_stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 