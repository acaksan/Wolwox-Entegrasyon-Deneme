from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    """Wolvox ürün modeli"""
    stok_kodu: str
    barkod: Optional[str]
    adi: str
    fiyat: float
    kdv_orani: float
    stok_miktari: float
    birim: str
    kategori: Optional[str]
    marka: Optional[str]
    updated_at: datetime 