"""Bağlantı test scripti"""

import os
import sys
from pathlib import Path

# Proje kök dizinini bul ve Python path'ine ekle
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio

from src.core.logging import logger
from src.core.settings import settings
from src.services.woocommerce_service import WooCommerceService


async def test_connections():
    """Tüm bağlantıları test eder"""
    logger.info(f"Python path: {sys.path}")
    logger.info(f"Çalışma dizini: {os.getcwd()}")
    
    # WooCommerce bağlantı testi
    try:
        woo_service = WooCommerceService()
        response = woo_service.wcapi.get("products", params={"per_page": 1})
        if response.status_code == 200:
            products = response.json()
            logger.info(f"✅ WooCommerce bağlantısı başarılı: {len(products)} ürün bulundu")
        else:
            logger.error(f"❌ WooCommerce bağlantı hatası: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"❌ WooCommerce bağlantı hatası: {str(e)}")
    
    # Firebird bağlantı testi
    try:
        import fdb
        conn = fdb.connect(
            host=settings.FIREBIRD_HOST,
            database=settings.FIREBIRD_DATABASE,
            user=settings.FIREBIRD_USER,
            password=settings.FIREBIRD_PASSWORD,
            charset=settings.FIREBIRD_CHARSET
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM RDB$DATABASE")
        logger.info("✅ Firebird bağlantısı başarılı")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"❌ Firebird bağlantı hatası: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connections()) 