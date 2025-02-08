import logging

import pytest
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)

class TestAPI:
    """API endpoint testleri"""
    
    def test_wolvox_products(self, test_client: TestClient):
        """Wolvox ürün endpoint testi"""
        try:
            response = test_client.get("/api/v1/wolvox/products/test")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            logger.info(f"Wolvox endpoint testi başarılı: {len(data)} ürün")
        except Exception as e:
            logger.error(f"Test hatası: {str(e)}")
            raise

    def test_woo_products(self, test_client: TestClient):
        """WooCommerce ürün endpoint testi"""
        try:
            response = test_client.get("/api/v1/woocommerce/products/test")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            logger.info(f"WooCommerce endpoint testi başarılı: {len(data)} ürün")
        except Exception as e:
            logger.error(f"Test hatası: {str(e)}")
            raise

    def test_comparison(self, test_client: TestClient):
        """Karşılaştırma endpoint testi"""
        try:
            response = test_client.get("/api/v1/products/comparison")
            assert response.status_code == 200
            data = response.json()
            
            # Response yapısını kontrol et
            assert "matched_count" in data
            assert "matched_wolvox" in data
            assert "matched_woo" in data
            assert "unmatched_wolvox" in data
            assert "unmatched_woo" in data
            
            logger.info(f"Karşılaştırma sonucu: {data['matched_count']} eşleşme")
        except Exception as e:
            logger.error(f"Test hatası: {str(e)}")
            raise 