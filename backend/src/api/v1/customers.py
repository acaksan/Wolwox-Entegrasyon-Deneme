# Müşteri entegrasyonu

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.utils.cache import cache_manager
from src.utils.logger import log_event
from src.wolvox.wolvox_service import WolvoxService

router = APIRouter()
wolvox_service = WolvoxService()

@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Tüm müşterileri listele."""
    try:
        # Cache kontrolü
        cache_key = f"customers_list_{skip}_{limit}"
        cached_customers = await cache_manager.get(cache_key)
        if cached_customers:
            return cached_customers

        customers = wolvox_service.get_customers(db, skip=skip, limit=limit)
        await cache_manager.set(cache_key, customers, expire=300)  # 5 dakika cache
        
        log_event("INFO", "customers", f"{len(customers)} müşteri listelendi")
        return customers
    except Exception as e:
        log_event("ERROR", "customers", "Müşteri listesi alınamadı", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteriler listelenirken bir hata oluştu"
        )

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Belirli bir müşteriyi getir."""
    try:
        # Cache kontrolü
        cache_key = f"customer_{customer_id}"
        cached_customer = await cache_manager.get(cache_key)
        if cached_customer:
            return cached_customer

        customer = wolvox_service.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Müşteri bulunamadı"
            )

        await cache_manager.set(cache_key, customer, expire=300)
        log_event("INFO", "customers", f"Müşteri detayı alındı: {customer_id}")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        log_event("ERROR", "customers", f"Müşteri detayı alınamadı: {customer_id}", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri detayı alınırken bir hata oluştu"
        )

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Yeni müşteri oluştur."""
    try:
        new_customer = wolvox_service.create_customer(db, customer)
        # Cache'i temizle
        await cache_manager.delete_pattern("customers_list_*")
        
        log_event("INFO", "customers", f"Yeni müşteri oluşturuldu: {new_customer.id}")
        return new_customer
    except Exception as e:
        log_event("ERROR", "customers", "Müşteri oluşturulamadı", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri oluşturulurken bir hata oluştu"
        )

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Müşteri güncelle."""
    try:
        updated_customer = wolvox_service.update_customer(db, customer_id, customer)
        if not updated_customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Müşteri bulunamadı"
            )

        # Cache'i temizle
        await cache_manager.delete(f"customer_{customer_id}")
        await cache_manager.delete_pattern("customers_list_*")
        
        log_event("INFO", "customers", f"Müşteri güncellendi: {customer_id}")
        return updated_customer
    except HTTPException:
        raise
    except Exception as e:
        log_event("ERROR", "customers", f"Müşteri güncellenemedi: {customer_id}", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri güncellenirken bir hata oluştu"
        )

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """Müşteri sil."""
    try:
        result = wolvox_service.delete_customer(db, customer_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Müşteri bulunamadı"
            )

        # Cache'i temizle
        await cache_manager.delete(f"customer_{customer_id}")
        await cache_manager.delete_pattern("customers_list_*")
        
        log_event("INFO", "customers", f"Müşteri silindi: {customer_id}")
    except HTTPException:
        raise
    except Exception as e:
        log_event("ERROR", "customers", f"Müşteri silinemedi: {customer_id}", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri silinirken bir hata oluştu"
        )

@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_customers(db: Session = Depends(get_db)):
    """WooCommerce ile müşteri senkronizasyonu."""
    try:
        result = await wolvox_service.sync_customers(db)
        # Tüm müşteri cache'lerini temizle
        await cache_manager.delete_pattern("customer_*")
        await cache_manager.delete_pattern("customers_list_*")
        
        log_event("INFO", "customers", "Müşteri senkronizasyonu tamamlandı", str(result))
        return {"message": "Müşteri senkronizasyonu başarıyla tamamlandı", "details": result}
    except Exception as e:
        log_event("ERROR", "customers", "Müşteri senkronizasyonu başarısız oldu", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Müşteri senkronizasyonu sırasında bir hata oluştu"
        )
