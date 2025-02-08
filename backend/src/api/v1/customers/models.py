"""Müşteri modelleri"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerGroup(str, Enum):
    """Müşteri grupları"""
    RETAIL = "retail"
    WHOLESALE = "wholesale"
    VIP = "vip"
    CORPORATE = "corporate"

class CustomerAddress(BaseModel):
    """Müşteri adres modeli"""
    
    id: Optional[int] = Field(None, description="Adres ID")
    type: str = Field(..., description="Adres tipi (fatura/teslimat)")
    address: str = Field(..., description="Adres")
    city: str = Field(..., description="Şehir")
    state: Optional[str] = Field(None, description="Bölge/Eyalet")
    country: str = Field(..., description="Ülke")
    postcode: str = Field(..., description="Posta kodu")
    phone: Optional[str] = Field(None, description="Telefon")
    
    class Config:
        from_attributes = True

class Customer(BaseModel):
    """Temel müşteri modeli"""
    musteri_kodu: str = Field(..., description="Müşteri kodu")
    musteri_adi: str = Field(..., description="Müşteri adı")
    vergi_no: Optional[str] = Field(None, description="Vergi numarası")
    vergi_dairesi: Optional[str] = Field(None, description="Vergi dairesi")
    adres: Optional[str] = Field(None, description="Adres")
    telefon: Optional[str] = Field(None, description="Telefon")
    email: Optional[str] = Field(None, description="E-posta")

class CustomerCreate(Customer):
    """Müşteri oluşturma modeli"""
    pass

class CustomerUpdate(Customer):
    """Müşteri güncelleme modeli"""
    musteri_kodu: Optional[str] = None
    musteri_adi: Optional[str] = None

class CustomerResponse(Customer):
    """Müşteri yanıt modeli"""
    wc_customer_id: Optional[int] = Field(None, description="WooCommerce müşteri ID")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Güncellenme tarihi")

    class Config:
        """Model ayarları"""
        from_attributes = True

# Modülleri dışa aktar
__all__ = ['Customer', 'CustomerGroup', 'CustomerAddress'] 