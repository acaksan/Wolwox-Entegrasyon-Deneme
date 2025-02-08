from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Temel ürün şeması."""
    name: str = Field(..., description="Ürün adı")
    description: Optional[str] = Field(None, description="Ürün açıklaması")
    sku: str = Field(..., description="Stok kodu")
    price: Decimal = Field(..., description="Satış fiyatı", ge=0)
    stock_quantity: int = Field(..., description="Stok miktarı", ge=0)
    category_id: Optional[int] = Field(None, description="Kategori ID")
    is_active: bool = Field(True, description="Ürün aktif mi?")

class ProductCreate(ProductBase):
    """Ürün oluşturma şeması."""
    pass

class ProductUpdate(ProductBase):
    """Ürün güncelleme şeması."""
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None

class ProductResponse(ProductBase):
    """Ürün yanıt şeması."""
    id: int
    woo_product_id: Optional[int] = Field(None, description="WooCommerce ürün ID")
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

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