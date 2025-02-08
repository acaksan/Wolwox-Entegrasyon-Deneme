import pytest
from services.woo_service import WooCommerceService


class TestWooService:
    def test_product_validation(self, mock_product):
        service = WooCommerceService()
        assert service.validate_product(mock_product) == True
    
    def test_order_processing(self, mock_order):
        service = WooCommerceService()
        assert service.process_order(mock_order) == True 