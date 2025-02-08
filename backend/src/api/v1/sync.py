"""Senkronizasyon API endpoint'leri"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services.sync_service import sync_service
from src.utils.logger import logger

router = APIRouter()

class SyncProductRequest(BaseModel):
    """Ürün senkronizasyon isteği"""
    stok_kodu: str

class SyncResponse(BaseModel):
    """Senkronizasyon yanıtı"""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """Hata yanıtı"""
    success: bool = False
    message: str
    error_code: str
    details: Optional[Dict[str, Any]] = None

@router.post("/products/{stok_kodu}", 
    response_model=SyncResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def sync_product(stok_kodu: str):
    """Tek bir ürünü senkronize et"""
    try:
        success = await sync_service.sync_product(stok_kodu)
        if not success:
            raise ValueError(f"Ürün senkronize edilemedi: {stok_kodu}")
            
        return SyncResponse(
            success=True,
            message=f"{stok_kodu} kodlu ürün başarıyla senkronize edildi"
        )
    except ValueError as e:
        logger.error(f"Ürün senkronizasyon hatası (validation): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        )
    except Exception as e:
        logger.exception(f"Ürün senkronizasyon hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Senkronizasyon hatası: {str(e)}",
                "error_code": "SYNC_ERROR"
            }
        )

@router.post("/products", 
    response_model=SyncResponse,
    responses={
        500: {"model": ErrorResponse}
    }
)
async def sync_all_products(batch_size: int = 10):
    """Tüm ürünleri senkronize et"""
    try:
        result = await sync_service.sync_all_products(batch_size)
        return SyncResponse(
            success=True,
            message="Ürün senkronizasyonu tamamlandı",
            details=result
        )
    except Exception as e:
        logger.exception(f"Toplu senkronizasyon hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Senkronizasyon hatası: {str(e)}",
                "error_code": "SYNC_ERROR"
            }
        )

@router.post("/stock/{stok_kodu}", 
    response_model=SyncResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def sync_stock(stok_kodu: str):
    """Stok miktarını senkronize et"""
    try:
        success = await sync_service.sync_stock(stok_kodu)
        if not success:
            raise ValueError(f"Stok senkronize edilemedi: {stok_kodu}")
            
        return SyncResponse(
            success=True,
            message=f"{stok_kodu} kodlu ürünün stok miktarı senkronize edildi"
        )
    except ValueError as e:
        logger.error(f"Stok senkronizasyon hatası (validation): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        )
    except Exception as e:
        logger.exception(f"Stok senkronizasyon hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Senkronizasyon hatası: {str(e)}",
                "error_code": "SYNC_ERROR"
            }
        )

@router.post("/orders/{order_id}", 
    response_model=SyncResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def sync_order(order_id: int):
    """Tek bir siparişi senkronize et"""
    try:
        success = await sync_service.sync_order(order_id)
        if not success:
            raise ValueError(f"Sipariş senkronize edilemedi: {order_id}")
            
        return SyncResponse(
            success=True,
            message=f"{order_id} numaralı sipariş başarıyla senkronize edildi"
        )
    except ValueError as e:
        logger.error(f"Sipariş senkronizasyon hatası (validation): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        )
    except Exception as e:
        logger.exception(f"Sipariş senkronizasyon hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Senkronizasyon hatası: {str(e)}",
                "error_code": "SYNC_ERROR"
            }
        )

@router.post("/orders", 
    response_model=SyncResponse,
    responses={
        500: {"model": ErrorResponse}
    }
)
async def sync_pending_orders():
    """Bekleyen siparişleri senkronize et"""
    try:
        result = await sync_service.sync_pending_orders()
        return SyncResponse(
            success=True,
            message="Bekleyen siparişler senkronize edildi",
            details=result
        )
    except Exception as e:
        logger.exception(f"Bekleyen sipariş senkronizasyon hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": f"Senkronizasyon hatası: {str(e)}",
                "error_code": "SYNC_ERROR"
            }
        )

@router.post("/customers/{customer_id}", 
    response_model=SyncResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def sync_customer(customer_id: int):
    """Tek bir müşteriyi senkronize et"""
    try:
        musteri_kodu = await sync_service.sync_customer(customer_id)
        return SyncResponse(
            success=True,
            message=f"{customer_id} numaralı müşteri başarıyla senkronize edildi",
            details={"musteri_kodu": musteri_kodu}
        )
    except ValueError as e:
        # İş kuralı ihlalleri
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        )
    except RuntimeError as e:
        # Teknik hatalar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "SYNC_ERROR"
            }
        )
    except Exception as e:
        # Beklenmeyen hatalar
        logger.exception("Beklenmeyen hata")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Beklenmeyen bir hata oluştu",
                "error_code": "INTERNAL_ERROR",
                "details": {"error": str(e)}
            }
        )

@router.get("/customers/find/{customer_id}", 
    response_model=SyncResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def find_or_create_customer(customer_id: int):
    """Müşteriyi bul veya oluştur"""
    try:
        musteri_kodu = await sync_service.get_or_create_customer(customer_id)
        return SyncResponse(
            success=True,
            message=f"{customer_id} numaralı müşteri bulundu veya oluşturuldu",
            details={"musteri_kodu": musteri_kodu}
        )
    except ValueError as e:
        # İş kuralı ihlalleri
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "VALIDATION_ERROR"
            }
        )
    except RuntimeError as e:
        # Teknik hatalar
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": str(e),
                "error_code": "SYNC_ERROR"
            }
        )
    except Exception as e:
        # Beklenmeyen hatalar
        logger.exception("Beklenmeyen hata")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "Beklenmeyen bir hata oluştu",
                "error_code": "INTERNAL_ERROR",
                "details": {"error": str(e)}
            }
        )
