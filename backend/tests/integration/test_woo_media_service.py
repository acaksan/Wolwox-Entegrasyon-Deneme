import asyncio
import json
import os
import ssl
import time
from pathlib import Path

import aiohttp
import pytest
import requests
import urllib3
from core.config import MediaServiceSettings
from core.logging import logger
from PIL import Image
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from services.woocommerce_media_service import (ImageProcessingError,
                                                WooCommerceMediaService)
from services.woocommerce_service import WooCommerceService

# SSL uyarılarını devre dışı bırak
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MockWooService:
    def __init__(self):
        self.wc_api_url = "http://example.com/wp-json/wc/v3"
        self.wp_api_url = "http://example.com/wp-json/wp/v2"
        self.wp_username = "test_user"
        self.wp_password = "test_pass"

    async def post(self, endpoint: str, data: any) -> dict:
        """Mock POST isteği"""
        if endpoint == "media":
            # FormData kontrolü
            if isinstance(data, (aiohttp.FormData, MockFormData)):
                return {
                    "id": 1,
                    "title": {"rendered": "Test Görsel"},
                    "alt_text": "Test Alt Text",
                    "caption": {"rendered": "Test Caption"},
                    "source_url": "http://example.com/test.jpg"
                }
            
        elif endpoint == "products":
            return {
                "id": 1,
                "images": data.get("images", [])
            }
        return {"error": "Invalid endpoint"}

    async def get(self, endpoint: str) -> dict:
        """Mock GET isteği"""
        if endpoint.startswith("products"):
            return {
                "id": 1,
                "images": []
            }
        return {"error": "Invalid endpoint"}

    async def get_product(self, product_id: int) -> dict:
        """Mock ürün getirme"""
        return {
            "id": product_id,
            "images": []
        }

    async def update_product(self, product_id: int, data: dict) -> dict:
        """Mock ürün güncelleme"""
        # Görsel sıralama için özel kontrol
        if "images" in data and len(data["images"]) > 0:
            image = data["images"][0]
            return {
                "id": product_id,
                "images": [{
                    "id": image["id"],
                    "src": "http://example.com/test.jpg",
                    "position": image.get("position", 0)
                }]
            }
        return {
            "id": product_id,
            "images": data.get("images", [])
        }

    async def delete(self, endpoint: str) -> dict:
        """Mock DELETE isteği"""
        return {"deleted": True}

    async def put(self, endpoint: str, data: dict) -> dict:
        """Mock PUT isteği"""
        if endpoint.startswith(f"{self.wc_api_url}/products/"):
            return {
                "id": int(endpoint.split('/')[-1]),
                "images": data.get("images", [])
            }
        return {"error": "Invalid endpoint"}

    async def get_media(self, media_id: int) -> dict:
        """Mock medya getirme"""
        return {
            "id": media_id,
            "title": {"rendered": "Test Görsel"},
            "alt_text": "Test Alt Text",
            "caption": {"rendered": "Test Caption"},
            "source_url": "http://example.com/test.jpg"
        }

class MockFormData:
    """Mock FormData sınıfı"""
    def __init__(self):
        self._fields = []
        
    def add_field(self, name: str, value: any, **kwargs):
        self._fields.append((name, value))
        
    def get(self, key: str, default: any = None):
        """FormData'dan veri alma"""
        for name, value in self._fields:
            if name == key:
                return value
        return default

@pytest.mark.asyncio
@pytest.mark.integration
class TestWooCommerceMedia:
    @pytest.fixture
    async def media_service(self):
        """Test için media servisi hazırlar"""
        service = WooCommerceMediaService(MockWooService())
        logger.info("✅ Test için media servisi hazırlandı")
        return service

    @pytest.fixture
    def test_image(self, tmp_path):
        """Test için geçici görsel oluşturur"""
        image_path = tmp_path / "test_image.jpg"
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image_path)
        return str(image_path)

    async def test_upload_image(self, media_service, test_image):
        """Temel görsel yükleme testi"""
        result = await media_service.upload_image(
            test_image,
            title="Test Görsel",
            alt_text="Test Alt Text",
            caption="Test Caption"
        )
        assert result["id"] == 1
        assert result["title"]["rendered"] == "Test Görsel"

    async def test_upload_image_with_seo(self, media_service, test_image):
        """SEO bilgileriyle görsel yükleme testi"""
        seo_data = {
            "title": "Test Görsel",
            "alt_text": "Test Alt Text",
            "description": "Test Açıklama"
        }
        result = await media_service.upload_image(
            test_image,
            **seo_data
        )
        assert result["title"]["rendered"] == seo_data["title"]

    async def test_get_product_images(self, media_service):
        """Ürün görsellerini getirme testi"""
        result = await media_service.get_product_images(1)
        assert isinstance(result, list)

    async def test_attach_image_to_product(self, media_service):
        """Görseli ürüne ekleme testi"""
        result = await media_service.attach_image_to_product(1, 1)
        assert result["images"][0]["id"] == 1

    async def test_image_validation(self, media_service, tmp_path):
        """Görsel doğrulama testi"""
        # Büyük dosya testi
        large_image_path = tmp_path / "large.jpg"
        img = Image.new('RGB', (5000, 5000), color='red')
        img.save(large_image_path, quality=100)
        
        # Dosya boyutunu kontrol et
        file_size = os.path.getsize(str(large_image_path)) / (1024 * 1024)  # MB
        if file_size <= media_service.max_file_size_mb:
            # Test için dosyayı büyüt
            with open(large_image_path, 'ab') as f:
                f.write(b'0' * int(10 * 1024 * 1024))  # 10MB ekle
        
        with pytest.raises(ImageProcessingError) as e:
            await media_service.upload_image(str(large_image_path))
        assert "boyutu çok büyük" in str(e.value)

        # Geçersiz format testi
        invalid_file = tmp_path / "test.txt"
        with open(invalid_file, 'w') as f:
            f.write("Bu bir görsel değil")
        
        with pytest.raises(ImageProcessingError) as e:
            await media_service.upload_image(str(invalid_file))
        assert "Desteklenmeyen dosya türü" in str(e.value)

    async def test_update_image_order(self, media_service, test_image):
        """Görsel sıralama testi"""
        image_result = await media_service.upload_image(test_image)
        result = await media_service.update_image_order(1, image_result["id"], 0)
        assert result["id"] == image_result["id"]

    async def test_upload_multiple_images(self, media_service, tmp_path):
        """Çoklu görsel yükleme testi"""
        image_paths = []
        for i in range(3):
            path = tmp_path / f"test_image_{i}.jpg"
            img = Image.new('RGB', (100, 100), color='red')
            img.save(path)
            image_paths.append(str(path))
        
        results = await media_service.bulk_upload_images(image_paths)
        assert len(results) == 3
        assert all(r["id"] == 1 for r in results)

    async def test_process_with_reporting(self, media_service, test_image):
        """İşlem raporlama testi"""
        report = await media_service.process_with_reporting(test_image)
        assert report["success"] is True
        assert len(report["steps"]) >= 3
        assert report["error"] is None
        
        # Hata senaryosu
        with pytest.raises(ImageProcessingError) as e:
            await media_service.process_with_reporting("nonexistent.jpg")
        assert e.value.details["error"]["type"] == "FileNotFoundError"

    async def test_rate_limiting(self, media_service, test_image):
        """Rate limiting testi"""
        start_time = time.time()
        tasks = []
        
        # Rate limit delay'i test için artır
        original_delay = media_service.rate_limit_delay
        media_service.rate_limit_delay = 0.3  # 300ms
        
        try:
            # 10 istek için toplam beklenen süre: 10 * 0.3 = 3 saniye
            for _ in range(10):
                task = asyncio.create_task(media_service.upload_image(test_image))
                tasks.append(task)
                await asyncio.sleep(0.2)  # İstekler arasında biraz daha bekle
            
            results = await asyncio.gather(*tasks)
            duration = time.time() - start_time
            
            # En az 2 saniye sürmeli
            assert duration >= 2, f"Rate limiting çalışmıyor: {duration:.2f} saniye sürdü"
            assert all(result["id"] == 1 for result in results)
        finally:
            # Rate limit delay'i geri al
            media_service.rate_limit_delay = original_delay
