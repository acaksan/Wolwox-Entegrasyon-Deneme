import asyncio
import logging
import random

import pytest
from core.config import get_settings
from core.exceptions import ServiceException
from core.metrics import registry, reset_metrics
from models.schemas import Product
from services.woocommerce_service import WooCommerceService

logger = logging.getLogger(__name__)

@pytest.fixture
async def woo_service():
    return WooCommerceService()

@pytest.fixture
def test_product():
    return Product(
        name="Test Ürün",
        sku=f"TEST{random.randint(1000,9999)}",
        price="100.00",
        stock_quantity=10
    )

@pytest.mark.integration
class TestWooCommerceIntegration:
    
    @pytest.fixture(autouse=True)
    async def setup_cleanup(self, woo_service):
        """Her test öncesi/sonrası temizlik"""
        self.woo_service = woo_service  # woo_service'i sınıf üyesi yap
        self.test_products = []
        reset_metrics()
        yield
        reset_metrics()
        # Temizlik
        for product in self.test_products:
            try:
                await self.woo_service.delete_product(product["id"])
            except Exception as e:
                logger.error(f"Ürün silme hatası: {str(e)}")
                continue
    
    @pytest.mark.integration
    async def test_connection(self, woo_service):
        """WooCommerce bağlantı testi"""
        try:
            # Basit bir API çağrısı yap
            response = await woo_service.get_products(per_page=1)
            assert isinstance(response, list)
            logger.info("✅ WooCommerce bağlantısı başarılı")
        except Exception as e:
            logger.error(f"❌ WooCommerce bağlantı hatası: {str(e)}")
            raise
    
    @pytest.mark.asyncio
    async def test_create_product(self, woo_service):
        """Ürün oluşturmayı test eder"""
        try:
            product_data = {
                "name": "Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "sku": f"TEST{random.randint(1000,9999)}",
                "manage_stock": True,
                "stock_quantity": 10,
                "status": "publish"
            }
            
            result = await woo_service.create_product(product_data)
            self.test_products.append(result)  # Temizlik için ekle
            
            assert result["name"] == product_data["name"]
            assert result["sku"] == product_data["sku"]
            return result["id"]
            
        except Exception as e:
            logger.error(f"Ürün oluşturma hatası: {str(e)}")
            raise
    
    @pytest.mark.asyncio
    async def test_update_product(self, woo_service):
        """Ürün güncellemeyi test eder"""
        product_id = None
        try:
            # Önce test ürünü oluştur
            product_data = {
                "name": "Update Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "sku": f"TEST{random.randint(1000,9999)}",
                "manage_stock": True,
                "stock_quantity": 10
            }
            
            created = await woo_service.create_product(product_data)
            self.test_products.append(created)
            product_id = created["id"]
            
            update_data = {
                "regular_price": "149.99",
                "stock_quantity": 20
            }
            
            result = await woo_service.update_product(product_id, update_data)
            assert float(result["regular_price"]) == float(update_data["regular_price"])
            assert result["stock_quantity"] == update_data["stock_quantity"]
            logger.info("✅ Ürün güncelleme başarılı!")
            
        except Exception as e:
            logger.error(f"❌ Ürün güncelleme hatası: {str(e)}")
            raise
    
    @pytest.mark.asyncio
    async def test_bulk_update(self, woo_service):
        """Toplu güncelleme testi"""
        test_products = [
            {
                "name": "Bulk Test 1",
                "type": "simple",
                "regular_price": "199.99",
                "sku": f"BULK{random.randint(1000,9999)}",
                "manage_stock": True,
                "stock_quantity": 5
            },
            {
                "name": "Bulk Test 2",
                "type": "simple", 
                "regular_price": "299.99",
                "sku": f"BULK{random.randint(1000,9999)}",
                "manage_stock": True,
                "stock_quantity": 10
            }
        ]
        
        created_products = []
        try:
            # Önce test ürünlerini oluştur
            for product in test_products:
                result = await woo_service.create_product(product)
                created_products.append(result)
                self.test_products.append(result)  # Temizlik için ekle
            
            # Güncelleme yap
            updates = [
                {
                    "id": product["id"],
                    "regular_price": "299.99",
                    "stock_quantity": 15
                }
                for product in created_products
            ]
            
            results = await woo_service.bulk_update_products(updates)
            assert len(results) == len(test_products)
            
        except Exception as e:
            logger.error(f"Bulk test hatası: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}")
    
    async def test_product_sync(self, woo_service):
        """Ürün senkronizasyonu testi"""
        try:
            # Test verisi
            product = {
                "name": "Test Ürün",
                "type": "simple",
                "regular_price": "99.99",
                "sku": f"TEST{random.randint(1000,9999)}"
            }
            
            # Oluştur
            created = await woo_service.create_product(product)
            self.test_products.append(created)
            
            # Kontrol
            fetched = await woo_service.get_product(created["id"])
            assert fetched["name"] == product["name"]
            assert fetched["sku"] == product["sku"]
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")
            
    async def test_order_sync(self, woo_service):
        """Sipariş senkronizasyonu testi"""
        try:
            # Test siparişi
            order = {
                "payment_method": "bacs",
                "payment_method_title": "Direct Bank Transfer",
                "status": "pending",
                "customer_note": "Test sipariş"
            }
            
            # Sipariş oluştur
            created = await woo_service.create_order(order)
            assert created["id"] > 0
            
            # Siparişi getir
            fetched = await woo_service.get_order(created["id"])
            assert fetched["status"] == order["status"]
            
            # Siparişi güncelle
            updated = await woo_service.update_order(created["id"], {"status": "processing"})
            assert updated["status"] == "processing"
            
        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_bulk_operations(self, woo_service):
        """Toplu işlemler testi"""
        try:
            # Test ürünlerini oluştur
            products = []
            for i in range(3):
                product = {
                    "name": f"Bulk Test {i}",
                    "type": "simple",
                    "regular_price": "99.99",
                    "sku": f"BULK{random.randint(1000,9999)}",
                    "manage_stock": True,
                    "stock_quantity": 10
                }
                result = await woo_service.create_product(product)
                products.append(result)
                self.test_products.append(result)
                
            # Toplu güncelleme
            updates = [
                {
                    "id": product["id"],
                    "regular_price": "149.99",
                    "stock_quantity": 20
                }
                for product in products
            ]
            
            results = await woo_service.bulk_update_products(updates)
            assert len(results) == len(products)
            
        except Exception as e:
            logger.error(f"❌ Bulk işlem hatası: {str(e)}")
            raise 