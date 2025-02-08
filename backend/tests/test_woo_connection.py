import asyncio

import pytest
from src.core.exceptions import ServiceException
from src.services.woocommerce_service import WooCommerceService


@pytest.mark.asyncio
async def test_woo_connection():
    """WooCommerce bağlantısını test eder"""
    try:
        service = WooCommerceService()
        async with service:
            # Ürünleri getirmeyi dene
            products = await service._make_request("GET", "products")
            assert products is not None
            assert isinstance(products, list)
            print(f"✅ WooCommerce bağlantısı başarılı. {len(products)} ürün bulundu.")
    except ServiceException as e:
        print(f"❌ WooCommerce bağlantı hatası: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {str(e)}")
        raise 
