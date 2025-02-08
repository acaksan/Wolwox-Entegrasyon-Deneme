import uuid
from datetime import datetime

import pytest
from core.logging import logger
from services.woocommerce_review_service import WooCommerceReviewService
from services.woocommerce_service import WooCommerceService


@pytest.fixture(scope="function")
async def review_service():
    """Test için review servisi hazırlar"""
    woo_service = WooCommerceService()
    service = WooCommerceReviewService(woo_service)
    logger.info("✅ Test için review servisi hazırlandı")
    return service

pytestmark = pytest.mark.asyncio

class TestWooCommerceReview:
    async def test_create_review(self, review_service, test_product):
        """Yorum oluşturma testi"""
        logger.info("🔍 Yorum oluşturma test ediliyor")
        
        unique_id = str(uuid.uuid4())
        test_review = {
            "product_id": test_product,
            "review": f"Test yorumu {unique_id}",
            "reviewer": "Test Kullanıcı",
            "reviewer_email": f"test{unique_id}@example.com",
            "rating": 5
        }
        
        result = await review_service.create_review(test_review)
        assert result["review"] == test_review["review"]
        logger.info(f"✅ Yorum oluşturuldu, ID: {result['id']}")
        return result["id"]
        
    async def test_update_review_status(self, review_service, test_product):
        """Yorum durumu güncelleme testi"""
        logger.info("🔍 Yorum durumu güncelleme test ediliyor")
        
        review_id = await self.test_create_review(review_service, test_product)
        result = await review_service.update_review_status(review_id, "approved")
        
        assert result["status"] == "approved"
        logger.info("✅ Yorum durumu güncellendi")
        
    async def test_get_reviews(self, review_service, test_product):
        """Yorumları listeleme testi"""
        logger.info("🔍 Yorumları listeleme test ediliyor")
        
        reviews = await review_service.get_reviews(
            product_id=test_product,
            status="approved"
        )
        
        assert isinstance(reviews, list)
        logger.info(f"✅ {len(reviews)} yorum listelendi")
        
    async def test_delete_review(self, review_service, test_product):
        """Yorum silme testi"""
        logger.info("🔍 Yorum silme test ediliyor")
        
        review_id = await self.test_create_review(review_service, test_product)
        result = await review_service.delete_review(review_id)
        
        assert result["deleted"] is True
        logger.info("✅ Yorum başarıyla silindi") 