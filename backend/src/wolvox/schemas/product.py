from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """
    Ürün şeması için temel sınıf
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)


class ProductCreate(ProductBase):
    """
    Ürün oluşturma şeması
    """
    wolvox_id: str = Field(..., min_length=1, max_length=50)
    wolvox_code: Optional[str] = Field(None, max_length=50)
    wolvox_barcode: Optional[str] = Field(None, max_length=50)


class ProductUpdate(ProductBase):
    """
    Ürün güncelleme şeması
    """
    woo_id: Optional[int] = None
    woo_sku: Optional[str] = Field(None, max_length=50)
    last_sync_status: Optional[str] = Field(None, max_length=50)
    last_sync_error: Optional[str] = Field(None, max_length=500)


class ProductInDB(ProductBase):
    """
    Veritabanındaki ürün şeması
    """
    id: int
    wolvox_id: str
    wolvox_code: Optional[str]
    wolvox_barcode: Optional[str]
    woo_id: Optional[int]
    woo_sku: Optional[str]
    last_sync_status: Optional[str]
    last_sync_error: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 