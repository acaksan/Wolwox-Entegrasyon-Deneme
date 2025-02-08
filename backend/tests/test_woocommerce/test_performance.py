import asyncio
import json
import time
from typing import Any, Dict

import pytest
from locust import HttpUser, between, task


@pytest.mark.performance
class TestPerformance:
    @pytest.fixture
    async def large_product_set(self):
        """Generate large product set for testing."""
        return [
            {
                "sku": f"PERF{i}",
                "name": f"Performance Test Product {i}",
                "regular_price": "99.90",
                "stock_quantity": 100
            }
            for i in range(1000)
        ]
    
    @pytest.mark.asyncio
    async def test_bulk_sync_performance(
        self,
        sync_service,
        large_product_set
    ):
        """Test bulk sync performance."""
        start_time = time.time()
        
        # Perform bulk sync
        results = await sync_service.bulk_sync_products(
            large_product_set,
            batch_size=100
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Assertions
        assert len(results) == len(large_product_set)
        assert duration < 60  # Should complete within 60 seconds
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, sync_service):
        """Test concurrent sync operations."""
        # Create multiple sync tasks
        tasks = [
            sync_service.sync_product({
                "sku": f"CONC{i}",
                "name": f"Concurrent Test {i}",
                "regular_price": "99.90"
            })
            for i in range(50)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        duration = time.time() - start_time
        
        # Assertions
        assert all(r.status == "success" for r in results)
        assert duration < 30  # Should complete within 30 seconds

class WooCommerceUser(HttpUser):
    wait_time = between(1, 3)  # Her request arası 1-3 sn bekle
    
    def on_start(self):
        """Her kullanıcı başladığında çalışır"""
        # Login ol ve token al
        response = self.client.post("/api/auth/login", json={
            "username": "test@example.com",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.environment.runner.quit()

    @task(3)
    def get_products(self):
        """Ürünleri listele"""
        self.client.get("/api/products", headers=self.headers)

    @task(2)
    def get_orders(self):
        """Siparişleri listele"""
        self.client.get("/api/orders", headers=self.headers)
        
    @task(1)
    def create_product(self):
        """Yeni ürün oluştur"""
        product_data = {
            "name": f"Test Ürün {time.time()}",
            "regular_price": "99.99",
            "description": "Test ürün açıklaması"
        }
        self.client.post("/api/products", 
                        json=product_data,
                        headers=self.headers)

    @task(1)
    def sync_products(self):
        """Ürün senkronizasyonu başlat"""
        self.client.post("/api/products/sync",
                        headers=self.headers)

# Locust komut satırından çalıştırma:
# locust -f tests/performance/test_performance.py --host=http://localhost:8000 