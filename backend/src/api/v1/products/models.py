"""Ürün modelleri"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ProductAttribute(BaseModel):
    """Ürün özellik modeli"""
    
    id: Optional[int] = Field(None, description="Özellik ID")
    name: str = Field(..., description="Özellik adı")
    value: str = Field(..., description="Özellik değeri")
    
    class Config:
        from_attributes = True

class ProductVariant(BaseModel):
    """Ürün varyant modeli"""
    
    id: Optional[int] = Field(None, description="Varyant ID")
    sku: str = Field(..., description="Stok kodu")
    barcode: Optional[str] = Field(None, description="Barkod")
    price: float = Field(..., description="Fiyat")
    stock: int = Field(..., description="Stok miktarı")
    attributes: List[ProductAttribute] = Field(default_factory=list, description="Özellikler")
    
    class Config:
        from_attributes = True

class Product(BaseModel):
    """Temel ürün modeli"""
    stok_kodu: str = Field(..., description="Stok kodu")
    stok_adi: str = Field(..., description="Ürün adı")
    barkod: Optional[str] = Field(None, description="Barkod")
    satis_fiyat1: float = Field(..., description="Satış fiyatı", ge=0)
    stok_miktari: float = Field(..., description="Stok miktarı", ge=0)
    birim: str = Field(..., description="Birim")
    kdv_orani: float = Field(..., description="KDV oranı", ge=0)
    grup_kodu: Optional[str] = Field(None, description="Grup kodu")
    marka_kodu: Optional[str] = Field(None, description="Marka kodu")

class ProductCreate(Product):
    """Ürün oluşturma modeli"""
    pass

class ProductUpdate(Product):
    """Ürün güncelleme modeli"""
    stok_kodu: Optional[str] = None
    stok_adi: Optional[str] = None
    satis_fiyat1: Optional[float] = None
    stok_miktari: Optional[float] = None
    birim: Optional[str] = None
    kdv_orani: Optional[float] = None

class ProductResponse(Product):
    """Ürün yanıt modeli"""
    wc_product_id: Optional[int] = Field(None, description="WooCommerce ürün ID")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Güncellenme tarihi")

    class Config:
        """Model ayarları"""
        from_attributes = True

__all__ = ['Product', 'ProductVariant', 'ProductAttribute']    