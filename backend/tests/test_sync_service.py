from unittest.mock import AsyncMock

import pytest
from models.schemas import Product
from services.sync_service import SyncService


@pytest.mark.asyncio
class TestSyncService:
    @pytest.fixture
    def mock_woo_service(self):
        return AsyncMock()
        
    @pytest.fixture
    def mock_firebird_service(self):
        return AsyncMock()
        
    @pytest.fixture
    def mock_message_queue(self):
        return AsyncMock()
        
    async def test_sync_products(
        self,
        mock_woo_service,
        mock_firebird_service,
        mock_message_queue
    ):
        # Arrange
        sync_service = SyncService(
            mock_woo_service,
            mock_firebird_service,
            mock_message_queue
        )
        
        mock_fb_products = [
            {
                "STOK_KODU": "TEST001",
                "STOK_ADI": "Test Ürün",
                "SATIS_FIYATI": "100.00",
                "MIKTAR": 10
            }
        ]
        
        mock_woo_products = [
            {
                "id": 1,
                "sku": "TEST001",
                "name": "Test Ürün"
            }
        ]
        
        mock_firebird_service.get_all.return_value = mock_fb_products
        mock_woo_service.get_products.return_value = mock_woo_products
        
        # Act
        await sync_service.sync_products(batch_size=10)
        
        # Assert
        mock_firebird_service.get_all.assert_called_once()
        mock_woo_service.get_products.assert_called_once()
        mock_message_queue.publish.assert_called()

@pytest.mark.asyncio
async def test_sync_products(sync_service):
    """Ürün senkronizasyonunu test eder"""
    await sync_service.sync_products(batch_size=10)
    # Assertions eklenebilir 