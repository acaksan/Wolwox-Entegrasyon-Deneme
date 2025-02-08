from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Sipariş durumu."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class OrderItemBase(BaseModel):
    """Temel sipariş kalemi şeması."""
    product_id: int = Field(..., description="Ürün ID")
    quantity: int = Field(..., description="Miktar", gt=0)
    unit_price: Decimal = Field(..., description="Birim fiyat", ge=0)

class OrderItemCreate(OrderItemBase):
    """Sipariş kalemi oluşturma şeması."""
    pass

class OrderItemResponse(OrderItemBase):
    """Sipariş kalemi yanıt şeması."""
    id: int
    total_price: Decimal
    product_name: str

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    """Temel sipariş şeması."""
    customer_id: int = Field(..., description="Müşteri ID")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Sipariş durumu")
    shipping_address: str = Field(..., description="Teslimat adresi")
    billing_address: str = Field(..., description="Fatura adresi")
    note: Optional[str] = Field(None, description="Sipariş notu")

class OrderCreate(OrderBase):
    """Sipariş oluşturma şeması."""
    items: List[OrderItemCreate] = Field(..., description="Sipariş kalemleri")

class OrderUpdate(BaseModel):
    """Sipariş güncelleme şeması."""
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    note: Optional[str] = None

class OrderResponse(OrderBase):
    """Sipariş yanıt şeması."""
    id: int
    woo_order_id: Optional[int] = Field(None, description="WooCommerce sipariş ID")
    items: List[OrderItemResponse]
    total_amount: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    customer_name: str

    class Config:
        from_attributes = True 