import asyncio
import json
import os
import tempfile

import aiohttp
import pytest
from core.config import MediaServiceSettings
from PIL import Image
from services.woocommerce_media_service import (ImageProcessingError,
                                                WooCommerceMediaService)


class MockFormData:
    def __init__(self):
        self._fields = []
        
    def add_field(self, name: str, value: str, **kwargs):
        self._fields.append((name, value))

class MockWooService:
    async def post(self, endpoint: str, data: dict) -> dict:
        if endpoint == "media":
            # Mock response
            return {
                "id": 1,
                "title": {"rendered": next((v for n,v in data._fields if n == "title"), "")},
                "alt_text": next((v for n,v in data._fields if n == "alt_text"), ""),
                "caption": {"rendered": next((v for n,v in data._fields if n == "caption"), "")},
                "source_url": "http://example.com/test.jpg"
            }
        return {"error": "Invalid endpoint"}

    async def update_product(self, product_id: int, data: dict) -> dict:
        return {
            "id": product_id,
            "images": data.get("images", [])
        }
        
    async def upload_media(self, file_path: str, **kwargs) -> dict:
        """Mock medya yükleme metodu"""
        return {
            "id": 1,
            "title": {"rendered": kwargs.get("title", "")},
            "alt_text": kwargs.get("alt_text", ""),
            "caption": {"rendered": kwargs.get("caption", "")},
            "source_url": "http://example.com/test.jpg",
            "media_type": "image",
            "mime_type": "image/jpeg",
            "status": "publish"
        }

@pytest.mark.asyncio
class TestWooMediaManual:
    @pytest.fixture
    async def media_service(self):
        service = WooCommerceMediaService(MockWooService())
        # Mock FormData
        service._create_form_data = lambda: MockFormData()
        return service

    @pytest.fixture
    def test_image(self):
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "test.jpg")
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image_path)
        return image_path

    async def test_upload_image(self, media_service, test_image):
        print("\n🔍 Test: Görsel Yükleme")
        try:
            result = await media_service.upload_image(
                test_image,
                title="Test Görsel",
                alt_text="Test Alt Text",
                caption="Test Caption"
            )
            assert result["id"] == 1
            assert result["title"]["rendered"] == "Test Görsel"
            print("✅ Görsel yükleme başarılı")
        except Exception as e:
            print(f"❌ Görsel yükleme başarısız: {str(e)}")
            raise

    async def test_upload_with_seo(self, media_service, test_image):
        print("\n🔍 Test: SEO ile Görsel Yükleme")
        try:
            seo_data = {
                "title": "SEO Test Görsel",
                "alt_text": "SEO Test Alt Text",
                "description": "SEO Test Description"
            }
            result = await media_service.upload_image(
                test_image,
                **seo_data
            )
            assert result["title"]["rendered"] == "SEO Test Görsel"
            print("✅ SEO ile görsel yükleme başarılı")
        except Exception as e:
            print(f"❌ SEO ile görsel yükleme başarısız: {str(e)}")
            raise

    async def test_safe_upload(self, media_service, test_image):
        print("\n🔍 Test: Güvenli Görsel Yükleme")
        try:
            result = await media_service.safe_upload(
                test_image,
                title="Safe Upload Test"
            )
            assert "error" not in result
            assert result["id"] == 1
            print("✅ Güvenli yükleme başarılı")
        except Exception as e:
            print(f"❌ Güvenli yükleme başarısız: {str(e)}")
            raise

    async def test_process_with_reporting(self, media_service, test_image):
        print("\n🔍 Test: İşlem Raporlama")
        try:
            # Başarılı senaryo
            report = await media_service.process_with_reporting(
                test_image,
                product_name="Test Ürün"
            )
            assert report["success"] is True
            assert len(report["steps"]) >= 3
            assert report["error"] is None
            print("✅ Başarılı senaryo testi geçti")

            # Hata senaryosu
            try:
                await media_service.process_with_reporting("nonexistent.jpg")
                print("❌ Hata senaryosu başarısız - hata yükseltilmedi")
            except ImageProcessingError:
                print("✅ Hata senaryosu başarılı - beklenen hata yükseltildi")
            
        except Exception as e:
            print(f"❌ İşlem raporlama testi başarısız: {str(e)}")
            raise

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 