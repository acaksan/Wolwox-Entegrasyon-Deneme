import os

import pytest
from core.logging import logger
from PIL import Image
from services.woocommerce_media_service import (ImageProcessingError,
                                                WooCommerceMediaService)


# Test Fixtures
@pytest.fixture(scope="module")
async def media_service(woo_service):
    """WooCommerce Media Service fixture"""
    service = WooCommerceMediaService(
        woo_service=woo_service,
        wp_username="wolvox",
        wp_password="Ac1476ac.!"
    )
    try:
        await service.test_connection()
        yield service
    finally:
        try:
            await service.cleanup()
        except Exception as e:
            logger.error(f"Media service cleanup hatası: {str(e)}")

@pytest.fixture(scope="function")
async def test_product(woo_service):
    """Test ürünü oluşturur"""
    product_data = {
        "name": "Test Ürünü",
        "type": "simple",
        "regular_price": "10.00",
        "description": "Test ürün açıklaması",
        "short_description": "Kısa açıklama"
    }
    
    try:
        response = await woo_service.create_product(product_data)
        product_id = response["id"]
        logger.info(f"✅ Test ürünü oluşturuldu: {product_id}")
        yield product_id
    finally:
        try:
            await woo_service.delete_product(product_id)
            logger.info(f"✅ Test ürünü silindi: {product_id}")
        except Exception as e:
            logger.error(f"Test ürünü silme hatası: {str(e)}")

@pytest.fixture(scope="function")
async def test_images(tmp_path):
    """Test görselleri oluşturur"""
    images = []
    try:
        for i in range(3):
            path = tmp_path / f"test_lastik_{i}.jpg"
            img = Image.new('RGB', (800, 800), color='red')
            img.save(path, quality=85)
            images.append(str(path))
        yield images
    finally:
        for path in images:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                logger.error(f"Test görsel temizleme hatası: {str(e)}")

# Test Cases
@pytest.mark.asyncio
@pytest.mark.integration
async def test_all_scenarios(media_service, test_product, test_images, tmp_path):
    """Tüm senaryoları test eder"""
    uploaded_ids = []
    
    try:
        # Watermark oluştur
        watermark_path = tmp_path / "watermark.png"
        watermark = Image.new('RGBA', (200, 200), (255, 255, 255, 128))
        watermark.save(watermark_path)
        logger.info("✅ Watermark görseli oluşturuldu")
        
        # 1. Temel görsel yükleme
        result = await media_service.safe_upload_image(
            test_images[0],
            product_name="Test Ürünü"
        )
        assert result["id"] > 0
        uploaded_ids.append(result["id"])
        logger.info("✅ Temel görsel yükleme başarılı")
        
        # 2. Watermark'lı yükleme
        result = await media_service.safe_upload_image(
            test_images[1],
            product_name="Test Ürünü",
            watermark_path=str(watermark_path)
        )
        assert result["id"] > 0
        uploaded_ids.append(result["id"])
        logger.info("✅ Watermark'lı yükleme başarılı")
        
        # 3. Toplu yükleme
        results = await media_service.bulk_upload_images(
            test_images,
            product_name="Test Ürünü"
        )
        assert len(results) == len(test_images)
        uploaded_ids.extend([r["id"] for r in results])
        logger.info("✅ Toplu yükleme başarılı")
        
        # 4. Hata senaryoları
        with pytest.raises(ImageProcessingError):
            large_image = tmp_path / "large.jpg"
            img = Image.new('RGB', (5000, 5000), color='red')
            img.save(large_image, quality=100)
            await media_service.safe_upload_image(str(large_image))
        logger.info("✅ Büyük dosya kontrolü başarılı")
        
    except Exception as e:
        logger.error(f"❌ Test hatası: {str(e)}")
        raise
    
    finally:
        # Temizlik
        for image_id in uploaded_ids:
            try:
                await media_service.delete_image(image_id)
            except Exception as e:
                logger.error(f"Görsel silme hatası (ID: {image_id}): {str(e)}")
        logger.info(f"✅ {len(uploaded_ids)} test görseli temizlendi") 