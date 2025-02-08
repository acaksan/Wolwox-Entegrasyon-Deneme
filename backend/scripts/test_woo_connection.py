import asyncio
import sys

from src.core.config import get_settings
from src.core.logging import logger
from src.services.woocommerce_service import WooCommerceService


async def test_connection():
    """WooCommerce bağlantısını test eder"""
    settings = get_settings()
    logger.info(f"WooCommerce URL: {settings.WOOCOMMERCE_URL}")
    
    try:
        service = WooCommerceService()
        
        # 1. Sistem durumu kontrolü
        logger.info("1. Sistem durumu kontrolü yapılıyor...")
        response = service.wcapi.get("system_status")
        if response.status_code == 200:
            logger.info("✅ Sistem durumu kontrolü başarılı")
        else:
            logger.error(f"❌ Sistem durumu hatası: {response.text}")
            return False
            
        # 2. Ürün listesi kontrolü
        logger.info("2. Ürün listesi kontrolü yapılıyor...")
        response = service.wcapi.get("products", params={"per_page": 1})
        if response.status_code == 200:
            products = response.json()
            logger.info(f"✅ Ürün listesi kontrolü başarılı: {len(products)} ürün")
        else:
            logger.error(f"❌ Ürün listesi hatası: {response.text}")
            return False
            
        # 3. API versiyon kontrolü
        logger.info("3. API versiyon kontrolü yapılıyor...")
        logger.info(f"✅ WooCommerce API Version: {settings.WOOCOMMERCE_VERSION}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Bağlantı hatası: {str(e)}")
        logger.debug("Detaylı hata:", exc_info=True)
        return False

if __name__ == "__main__":
    logger.info("🔌 WooCommerce Bağlantı Testi Başlatılıyor...")
    
    result = asyncio.run(test_connection())
    
    if not result:
        logger.error("❌ Test başarısız!")
        sys.exit(1)
    
    logger.info("✨ Tüm testler başarılı!")
    sys.exit(0) 