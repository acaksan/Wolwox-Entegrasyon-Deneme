"""Senkronizasyon servisi.

Bu modül, Wolvox ve WooCommerce arasındaki senkronizasyon işlemlerini yönetir.
"""

from typing import Dict, Any, Optional
from core.logger import logger
from core.config import get_sync_settings
from services.woocommerce_service import WooCommerceService
from services.wolvox_product_service import WolvoxProductService


class SyncService:
    """Senkronizasyon servisi sınıfı.
    
    Bu sınıf, Wolvox ve WooCommerce arasındaki ürün, stok ve sipariş 
    senkronizasyonunu yönetir.
    """

    def __init__(self) -> None:
        """Servis başlatıcı.
        
        WooCommerce ve Wolvox servislerini başlatır ve senkronizasyon ayarlarını alır.
        """
        self.woo = WooCommerceService()
        self.wolvox = WolvoxProductService()
        self.settings = get_sync_settings()

    async def sync_products(self) -> bool:
        """Ürünleri senkronize et.
        
        Returns:
            bool: Senkronizasyon başarılı ise True, değilse False
            
        Raises:
            Exception: Senkronizasyon sırasında oluşan hatalar
        """
        try:
            # Wolvox'tan ürünleri al
            wolvox_products = await self.wolvox.get_products()
            
            # Her bir ürün için
            for product in wolvox_products:
                # WooCommerce'da ürünü güncelle veya oluştur
                await self.woo.update_or_create_product(product)
                
            logger.info(f"{len(wolvox_products)} ürün başarıyla senkronize edildi")
            return True
        except Exception as e:
            logger.error(f"Ürün senkronizasyonu sırasında hata: {str(e)}")
            raise

    async def sync_stock(self) -> bool:
        """Stok bilgilerini senkronize et.
        
        Returns:
            bool: Senkronizasyon başarılı ise True, değilse False
            
        Raises:
            Exception: Senkronizasyon sırasında oluşan hatalar
        """
        try:
            # Wolvox'tan ürünleri al
            wolvox_products = await self.wolvox.get_products()
            
            # Her bir ürün için
            for product in wolvox_products:
                # WooCommerce'da stok bilgisini güncelle
                await self.woo.update_stock(product['stokkodu'], product['stok_miktari'])
                
            logger.info(f"{len(wolvox_products)} ürünün stok bilgisi başarıyla senkronize edildi")
            return True
        except Exception as e:
            logger.error(f"Stok senkronizasyonu sırasında hata: {str(e)}")
            raise

    async def sync_orders(self) -> bool:
        """Siparişleri senkronize et.
        
        Returns:
            bool: Senkronizasyon başarılı ise True, değilse False
            
        Raises:
            Exception: Senkronizasyon sırasında oluşan hatalar
        """
        try:
            # WooCommerce'dan yeni siparişleri al
            orders = await self.woo.get_new_orders()
            
            # Her bir sipariş için
            for order in orders:
                # Wolvox'ta siparişi oluştur
                await self.wolvox.create_order(order)
                
            logger.info(f"{len(orders)} sipariş başarıyla senkronize edildi")
            return True
        except Exception as e:
            logger.error(f"Sipariş senkronizasyonu sırasında hata: {str(e)}")
            raise 