"""Müşteri servisi"""

import logging
from typing import Any, Dict, List

from src.core.exceptions import ServiceError

from .base_service import BaseService

logger = logging.getLogger(__name__)

class CustomerService(BaseService):
    """Müşteri servisi"""
    
    async def get_customers(self) -> List[Dict[str, Any]]:
        """Müşterileri getir"""
        try:
            # TODO: Implement customer list retrieval
            return []
        except Exception as e:
            logger.error(f"❌ Müşteri listesi alınamadı: {str(e)}")
            raise ServiceError(f"Müşteri listesi alınamadı: {str(e)}")
    
    async def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Müşteri detayı getir"""
        try:
            # TODO: Implement customer detail retrieval
            return {}
        except Exception as e:
            logger.error(f"❌ Müşteri detayı alınamadı: {str(e)}")
            raise ServiceError(f"Müşteri detayı alınamadı: {str(e)}")

# Singleton instance
customer_service = CustomerService()

__all__ = ['CustomerService', 'customer_service'] 