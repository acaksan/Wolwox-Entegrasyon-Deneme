"""Sipariş modelleri"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Sipariş durumları"""
    NEW = "new"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    FAILED = "failed"
    ON_HOLD = "on-hold"

class OrderItem(BaseModel):
    """Sipariş kalemi modeli"""
    stok_kodu: str = Field(..., description="Stok kodu")
    miktar: float = Field(..., description="Miktar", ge=0)
    fiyat: float = Field(..., description="Birim fiyat", ge=0)
    kdv_orani: float = Field(..., description="KDV oranı", ge=0)

class Order(BaseModel):
    """Temel sipariş modeli"""
    musteri_kodu: str = Field(..., description="Müşteri kodu")
    musteri_adi: str = Field(..., description="Müşteri adı")
    tutar: float = Field(..., description="Tutar", ge=0)
    kdv: float = Field(..., description="KDV", ge=0)
    toplam: float = Field(..., description="Toplam tutar", ge=0)
    durum: str = Field(..., description="Sipariş durumu")
    kalemler: List[OrderItem] = Field(..., description="Sipariş kalemleri")

class OrderCreate(Order):
    """Sipariş oluşturma modeli"""
    pass

class OrderUpdate(Order):
    """Sipariş güncelleme modeli"""
    musteri_kodu: Optional[str] = None
    musteri_adi: Optional[str] = None
    tutar: Optional[float] = None
    kdv: Optional[float] = None
    toplam: Optional[float] = None
    durum: Optional[str] = None
    kalemler: Optional[List[OrderItem]] = None

class OrderResponse(Order):
    """Sipariş yanıt modeli"""
    siparis_no: str = Field(..., description="Sipariş numarası")
    wc_order_id: Optional[int] = Field(None, description="WooCommerce sipariş ID")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Güncellenme tarihi")

    class Config:
        """Model ayarları"""
        from_attributes = True

__all__ = ['Order', 'OrderItem', 'OrderStatus'] 