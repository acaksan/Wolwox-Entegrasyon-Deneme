"""WooCommerce API servisi"""

from typing import Any, Dict, List, Optional

from src.core.exceptions import WooCommerceException
from src.core.logging import logger
from src.core.settings import get_settings
from woocommerce import API

settings = get_settings()

class WooCommerceService:
    """WooCommerce API servis sınıfı"""
    
    def __init__(self):
        """WooCommerce API istemcisini başlat"""
        try:
            self.client = API(
                url=settings.WOO_URL,
                consumer_key=settings.WOO_CONSUMER_KEY,
                consumer_secret=settings.WOO_CONSUMER_SECRET,
                version="wc/v3"
            )
            self.logger = logger
        except Exception as e:
            self.logger.error(f"WooCommerce API bağlantı hatası: {str(e)}")
            raise WooCommerceException(f"WooCommerce API bağlantı hatası: {str(e)}")

    async def get_products(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        WooCommerce'den ürünleri getir
        
        Args:
            page: Sayfa numarası
            per_page: Sayfa başına ürün sayısı
            search: Arama terimi
            
        Returns:
            List[Dict]: Ürün listesi
            
        Raises:
            WooCommerceException: API hatası durumunda
        """
        try:
            params = {
                "page": page,
                "per_page": per_page
            }
            
            if search:
                params["search"] = search
                
            response = self.client.get("products", params=params)
            
            if response.status_code != 200:
                raise WooCommerceException(
                    f"Ürün getirme hatası: {response.text}"
                )
                
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Ürün getirme hatası: {str(e)}")
            raise WooCommerceException(f"Ürün getirme hatası: {str(e)}")

    async def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        WooCommerce'den tek ürün getir
        
        Args:
            product_id: Ürün ID
            
        Returns:
            Dict: Ürün detayları
            
        Raises:
            WooCommerceException: API hatası durumunda
        """
        try:
            response = self.client.get(f"products/{product_id}")
            
            if response.status_code != 200:
                raise WooCommerceException(
                    f"Ürün getirme hatası: {response.text}"
                )
                
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Ürün getirme hatası: {str(e)}")
            raise WooCommerceException(f"Ürün getirme hatası: {str(e)}")

    async def update_product(
        self,
        product_id: Optional[int],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        WooCommerce'de ürün güncelle veya oluştur
        
        Args:
            product_id: Ürün ID (None ise yeni ürün oluşturur)
            data: Ürün verileri
            
        Returns:
            Dict: Güncellenmiş/oluşturulmuş ürün
            
        Raises:
            WooCommerceException: API hatası durumunda
        """
        try:
            if product_id:
                response = self.client.put(f"products/{product_id}", data)
            else:
                response = self.client.post("products", data)
                
            if response.status_code not in [200, 201]:
                raise WooCommerceException(
                    f"Ürün güncelleme hatası: {response.text}"
                )
                
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Ürün güncelleme hatası: {str(e)}")
            raise WooCommerceException(f"Ürün güncelleme hatası: {str(e)}")

wc_service = WooCommerceService()

__all__ = ['WooCommerceService', 'wc_service'] 