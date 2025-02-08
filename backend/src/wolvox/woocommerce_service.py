"""WooCommerce API servisi"""

from typing import Any, Dict, List, Optional

import aiohttp
from src.core.settings import get_settings
from src.utils.logger import logger

settings = get_settings()

class WooCommerceService:
    """WooCommerce API servisi"""
    
    def __init__(self):
        """WooCommerce API bağlantısını başlat"""
        self.base_url = settings.WC_URL.rstrip("/")
        self.auth = (settings.WC_CONSUMER_KEY, settings.WC_CONSUMER_SECRET)
        self.verify_ssl = settings.WC_VERIFY_SSL
        self.version = settings.WC_VERSION.replace("wc/v", "")  # "wc/v3" -> "3"
        
    def _get_url(self, endpoint: str) -> str:
        """API endpoint URL'ini oluştur"""
        return f"{self.base_url}/wp-json/wc/v{self.version}/{endpoint.lstrip('/')}"
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """API isteği yap"""
        url = self._get_url(endpoint)
        logger.debug(f"WooCommerce API isteği: {method} {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    auth=aiohttp.BasicAuth(*self.auth),
                    ssl=self.verify_ssl,
                    **kwargs
                ) as response:
                    if response.status == 404:
                        logger.error(f"Kaynak bulunamadı: {url}")
                        return None
                    
                    data = await response.json()
                    
                    if response.status >= 400:
                        error_msg = data.get('message', 'Bilinmeyen hata')
                        logger.error(f"WooCommerce API hatası: {error_msg}")
                        raise RuntimeError(f"WooCommerce API hatası: {error_msg}")
                    
                    logger.debug(f"WooCommerce API yanıtı: {response.status}")
                    return data
                    
        except aiohttp.ClientError as e:
            logger.error(f"WooCommerce API bağlantı hatası: {str(e)}")
            raise RuntimeError(f"WooCommerce API bağlantı hatası: {str(e)}")
        except Exception as e:
            logger.error(f"WooCommerce API beklenmeyen hata: {str(e)}")
            raise RuntimeError(f"WooCommerce API beklenmeyen hata: {str(e)}")
    
    async def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """WooCommerce'den müşteri bilgilerini getir"""
        return await self._make_request("GET", f"customers/{customer_id}")
    
    async def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """WooCommerce'den sipariş bilgilerini getir"""
        return await self._make_request("GET", f"orders/{order_id}")
    
    async def get_orders(self, **params) -> Dict[str, Any]:
        """WooCommerce'den siparişleri getir"""
        return await self._make_request("GET", "orders", params=params)
    
    async def get_products(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """WooCommerce'den ürünleri getir"""
        return await self._make_request(
            "GET",
            "products",
            params={"page": page, "per_page": per_page}
        )
    
    async def create_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """WooCommerce'de yeni ürün oluştur"""
        return await self._make_request("POST", "products", json=product_data)
    
    async def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """WooCommerce'de ürün güncelle"""
        return await self._make_request("PUT", f"products/{product_id}", json=product_data)
    
    async def update_stock(self, product_id: int, quantity: int) -> Optional[Dict[str, Any]]:
        """WooCommerce'de stok miktarını güncelle"""
        return await self._make_request(
            "PUT",
            f"products/{product_id}",
            json={"stock_quantity": quantity}
        )

# Servis örneği
woocommerce_service = WooCommerceService()
