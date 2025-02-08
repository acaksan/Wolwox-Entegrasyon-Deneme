"""Müşteri API endpoint'leri"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.utils.logger import logger
from src.wolvox.wolvox_service import WolvoxService


class CustomerResponse(BaseModel):
    """Müşteri yanıt şeması"""
    musteri_kodu: str
    unvan: str
    vergi_no: Optional[str] = None
    vergi_dairesi: Optional[str] = None
    adres: Optional[str] = None
    telefon: Optional[str] = None
    email: Optional[str] = None

class CustomerMeta(BaseModel):
    """Sayfalama meta bilgileri"""
    total: int
    page: int
    limit: int
    pages: int

class CustomerList(BaseModel):
    """Müşteri listesi şeması"""
    data: List[CustomerResponse]
    meta: CustomerMeta

# Router'ı oluştur
router = APIRouter(prefix="/customers", tags=["customers"])

# Wolvox servisini başlat
wolvox_service = WolvoxService()

@router.get("/wolvox", response_model=CustomerList)
async def get_wolvox_customers(
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    limit: int = Query(10, ge=1, le=100, description="Sayfa başına müşteri sayısı"),
    search: Optional[str] = Query(None, description="Arama terimi (müşteri kodu veya adı)")
):
    """
    Wolvox'tan müşterileri getir
    
    Args:
        page: Sayfa numarası
        limit: Sayfa başına müşteri sayısı
        search: Arama terimi
        
    Returns:
        CustomerList: Müşteri listesi ve meta bilgiler
    """
    try:
        # Müşterileri getir
        customers = await wolvox_service.get_customers(
            page=page,
            limit=limit,
            search=search
        )
        
        # Toplam müşteri sayısını al
        total = await wolvox_service.get_customer_count(search)
        
        return CustomerList(
            data=customers,
            meta=CustomerMeta(
                total=total,
                page=page,
                limit=limit,
                pages=(total + limit - 1) // limit
            )
        )
        
    except Exception as e:
        logger.error(f"Müşteri getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Müşteri getirme hatası: {str(e)}"
        )

@router.get("/wolvox/{musteri_kodu}", response_model=CustomerResponse)
async def get_wolvox_customer(musteri_kodu: str):
    """
    Wolvox'tan tek müşteri getir
    
    Args:
        musteri_kodu: Müşteri kodu
        
    Returns:
        CustomerResponse: Müşteri detayları
    """
    try:
        customer = await wolvox_service.get_customer(musteri_kodu)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail=f"Müşteri bulunamadı: {musteri_kodu}"
            )
        return CustomerResponse(**customer)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Müşteri getirme hatası: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Müşteri getirme hatası: {str(e)}"
        )

@router.get("/woocommerce")
async def get_wc_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """WooCommerce müşterilerini listele"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_customers(page=page, per_page=per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/woocommerce/{customer_id}")
async def get_wc_customer(customer_id: int) -> Dict[str, Any]:
    """WooCommerce müşteri detayı getir"""
    try:
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        return await wc_service.get_customer(customer_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sync/{customer_code}")
async def sync_customer(customer_code: str) -> Dict[str, Any]:
    """Wolvox'tan WooCommerce'e müşteri senkronizasyonu"""
    try:
        # Wolvox'tan müşteri bilgilerini al
        wolvox_customer = await wolvox_service.get_customer(customer_code)
        if not wolvox_customer:
            raise HTTPException(status_code=404, detail="Wolvox müşterisi bulunamadı")

        # WooCommerce'de güncelle/oluştur
        from src.api.v1.woocommerce.woocommerce_service import wc_service
        wc_customer = await wc_service.update_customer(
            customer_id=wolvox_customer.get("wc_customer_id"),  # Eğer varsa
            data={
                "email": wolvox_customer.get("email", ""),
                "first_name": wolvox_customer["unvan"].split()[0],
                "last_name": " ".join(wolvox_customer["unvan"].split()[1:]),
                "billing": {
                    "first_name": wolvox_customer["unvan"].split()[0],
                    "last_name": " ".join(wolvox_customer["unvan"].split()[1:]),
                    "company": wolvox_customer.get("vergi_no", ""),
                    "address_1": wolvox_customer.get("adres", ""),
                    "phone": wolvox_customer.get("telefon", ""),
                    "email": wolvox_customer.get("email", "")
                }
            }
        )

        return {
            "wolvox_customer": wolvox_customer,
            "wc_customer": wc_customer
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 