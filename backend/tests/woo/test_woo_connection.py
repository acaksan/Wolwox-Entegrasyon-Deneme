import pytest
from woocommerce import API


class TestWooConnection:
    def setup_method(self):
        self.wcapi = API(
            url="http://localhost:8000",
            consumer_key="test_key",
            consumer_secret="test_secret",
            version="wc/v3"
        )
    
    def test_connection(self):
        """WooCommerce API bağlantı testi"""
        response = self.wcapi.get("products")
        assert response.status_code == 200
    
    def test_get_products(self):
        """Ürün listesi çekme testi"""
        response = self.wcapi.get("products")
        products = response.json()
        assert isinstance(products, list)
        
    def test_get_orders(self):
        """Sipariş listesi çekme testi"""
        response = self.wcapi.get("orders")
        orders = response.json()
        assert isinstance(orders, list) 