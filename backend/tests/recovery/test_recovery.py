import asyncio
from datetime import datetime

import docker
import pytest
from core.exceptions import ServiceException
from core.logging import logger
from core.security import create_test_token
from httpx import AsyncClient
from main import app

from backend.services import WolvoxService, WooCommerceService


class TestRecovery:
    @pytest.fixture
    async def client(self):
        """Test client."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            token = create_test_token()
            client.headers["Authorization"] = f"Bearer {token}"
            yield client
    
    @pytest.fixture
    def docker_client(self):
        """Docker client."""
        return docker.from_env()

    async def _wait_for_healthy(self, client, max_retries=30, delay=1):
        """Servisin sağlıklı olmasını bekle."""
        for _ in range(max_retries):
            try:
                response = await client.get("/health")
                if response.status_code == 200:
                    return True
            except Exception:
                pass
            await asyncio.sleep(delay)
        return False

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_database_recovery(self, client, docker_client):
        """Veritabanı recovery testi."""
        # 1. Test verisi oluştur
        response = await client.post("/api/v1/products", json={
            "sku": "RECOVERY_TEST",
            "name": "Recovery Test Product",
            "price": "99.90"
        })
        assert response.status_code == 201
        product_id = response.json()["id"]

        # 2. Veritabanı container'ını yeniden başlat
        db_container = docker_client.containers.get("woocommerce-wolvox_db_1")
        db_container.restart()

        # 3. Sistemin recovery olmasını bekle
        assert await self._wait_for_healthy(client)

        # 4. Veri tutarlılığını kontrol et
        response = await client.get(f"/api/v1/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["sku"] == "RECOVERY_TEST"

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_cache_recovery(self, client, docker_client):
        """Cache recovery testi."""
        # 1. Cache'e veri yaz
        await client.get("/api/v1/products/popular")  # Cache'e yaz
        
        # 2. Redis container'ını yeniden başlat
        redis_container = docker_client.containers.get("woocommerce-wolvox_redis_1")
        redis_container.restart()

        # 3. Recovery'i bekle
        await asyncio.sleep(5)

        # 4. Cache yeniden oluşturulmalı
        response = await client.get("/api/v1/products/popular")
        assert response.status_code == 200
        assert "X-Cache" in response.headers

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_sync_recovery(self, client):
        """Senkronizasyon recovery testi."""
        # 1. Senkronizasyonu başlat ve yarıda kes
        response = await client.post("/api/v1/sync/products")
        job_id = response.json()["job_id"]
        
        # 2. Uygulamayı yeniden başlat (simüle et)
        await app.shutdown()
        await app.startup()

        # 3. Senkronizasyon kaldığı yerden devam etmeli
        response = await client.get(f"/api/v1/sync/status/{job_id}")
        assert response.status_code == 200
        assert response.json()["status"] in ["completed", "in_progress"]

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_network_partition(self, client, docker_client):
        """Network partition recovery testi."""
        # 1. Network partition simüle et
        network = docker_client.networks.get("woocommerce-wolvox_default")
        network.disconnect("woocommerce-wolvox_app_1")

        # 2. İşlem dene
        response = await client.post("/api/v1/products", json={
            "sku": "NETWORK_TEST",
            "name": "Network Test Product",
            "price": "99.90"
        })
        assert response.status_code in [503, 500]  # Servis kullanılamaz olmalı

        # 3. Network'ü düzelt
        network.connect("woocommerce-wolvox_app_1")

        # 4. Sistem kendini toparlamalı
        assert await self._wait_for_healthy(client)

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_data_consistency_recovery(self, client):
        """Veri tutarlılığı recovery testi."""
        woo_service = WooCommerceService()
        wolvox_service = WolvoxService()

        # 1. Tutarsız durum oluştur
        test_sku = "CONSISTENCY_TEST"
        woo_stock = 100
        wolvox_stock = 50

        # WooCommerce'de farklı stok
        await woo_service.update_product_stock(test_sku, woo_stock)
        # Wolvox'ta farklı stok
        await wolvox_service.update_stock(test_sku, wolvox_stock)

        # 2. Consistency check başlat
        response = await client.post("/api/v1/system/check-consistency")
        assert response.status_code == 200

        # 3. Sistem tutarsızlığı düzeltmeli
        await asyncio.sleep(5)  # Recovery için bekle

        # 4. Stoklar eşleşmeli
        woo_product = await woo_service.get_product_by_sku(test_sku)
        assert woo_product["stock_quantity"] == wolvox_stock  # Wolvox stoku geçerli olmalı

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_queue_recovery(self, client, docker_client):
        """Message queue recovery testi."""
        # 1. Uzun sürecek görevler oluştur
        tasks = []
        for i in range(10):
            response = await client.post("/api/v1/tasks/long-running", json={
                "task_id": f"recovery_{i}",
                "duration": 30
            })
            tasks.append(response.json()["task_id"])

        # 2. RabbitMQ'yu yeniden başlat
        rabbitmq_container = docker_client.containers.get("woocommerce-wolvox_rabbitmq_1")
        rabbitmq_container.restart()

        # 3. Recovery'i bekle
        await asyncio.sleep(10)

        # 4. Tüm taskler kaldığı yerden devam etmeli
        for task_id in tasks:
            response = await client.get(f"/api/v1/tasks/{task_id}")
            assert response.json()["status"] != "failed"

    @pytest.mark.recovery
    @pytest.mark.asyncio
    async def test_partial_system_failure(self, client, docker_client):
        """Kısmi sistem hatası recovery testi."""
        # 1. Bazı servisleri durdur
        services = ["redis", "rabbitmq"]
        for service in services:
            container = docker_client.containers.get(f"woocommerce-wolvox_{service}_1")
            container.stop()

        # 2. Sistem kısmi çalışmaya devam etmeli
        response = await client.get("/api/v1/products")
        assert response.status_code == 200  # Temel fonksiyonlar çalışmalı

        # 3. Servisleri geri getir
        for service in services:
            container = docker_client.containers.get(f"woocommerce-wolvox_{service}_1")
            container.start()

        # 4. Tam fonksiyonellik geri gelmeli
        assert await self._wait_for_healthy(client) 

    @pytest.mark.recovery
    async def test_connection_recovery(self, woo_service):
        """Bağlantı kopması durumunda recovery testi"""
        try:
            # Bağlantıyı test et
            await woo_service.get_products(per_page=1)
            
            # Bağlantıyı kapat
            woo_service.wcapi.close()
            
            # Yeni istek yap - otomatik yeniden bağlanmalı
            products = await woo_service.get_products(per_page=1)
            assert isinstance(products, list)
            
        except Exception as e:
            logger.error(f"❌ Recovery test hatası: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}")
            
    @pytest.mark.recovery
    async def test_error_recovery(self, woo_service):
        """Hata durumunda recovery testi"""
        try:
            # Hatalı istek yap
            with pytest.raises(ServiceException):
                await woo_service.get_product(999999)
                
            # Normal istek yap - servis çalışmaya devam etmeli
            products = await woo_service.get_products(per_page=1)
            assert isinstance(products, list)
            
        except Exception as e:
            logger.error(f"❌ Error recovery test hatası: {str(e)}")
            pytest.fail(f"Test failed: {str(e)}") 