"""SyncService testleri."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from services.sync_service import SyncService


@pytest.fixture
def mock_woo_service():
    """Mock WooCommerceService fixture'ı."""
    mock = Mock()
    mock.get_new_orders = AsyncMock()
    mock.update_or_create_product = AsyncMock()
    mock.update_stock = AsyncMock()
    return mock


@pytest.fixture
def mock_wolvox_service():
    """Mock WolvoxProductService fixture'ı."""
    mock = Mock()
    mock.get_products = AsyncMock()
    mock.create_order = AsyncMock()
    return mock


@pytest.fixture
def mock_settings():
    """Mock senkronizasyon ayarları fixture'ı."""
    return Mock()


@pytest.fixture
def service(mock_woo_service, mock_wolvox_service, mock_settings):
    """SyncService fixture'ı."""
    with patch("services.sync_service.WooCommerceService", return_value=mock_woo_service), \
         patch("services.sync_service.WolvoxProductService", return_value=mock_wolvox_service), \
         patch("services.sync_service.get_sync_settings", return_value=mock_settings):
        service = SyncService()
        return service


@pytest.mark.asyncio
async def test_sync_products_success(service, mock_woo_service, mock_wolvox_service):
    """sync_products başarılı durumu testi."""
    # Test verileri
    mock_products = [
        {
            "stokkodu": "TEST001",
            "stok_adi": "Test Ürün",
            "stok_miktari": 10,
            "satis_fiyati": 100
        }
    ]
    
    # Mock ayarları
    mock_wolvox_service.get_products.return_value = mock_products
    mock_woo_service.update_or_create_product.return_value = True
    
    # Test
    result = await service.sync_products()
    
    # Doğrulamalar
    assert result is True
    mock_wolvox_service.get_products.assert_called_once()
    mock_woo_service.update_or_create_product.assert_called_once_with(mock_products[0])


@pytest.mark.asyncio
async def test_sync_products_error(service, mock_wolvox_service):
    """sync_products hata durumu testi."""
    # Mock ayarları
    mock_wolvox_service.get_products.side_effect = Exception("Sync Error")
    
    # Test ve doğrulama
    with pytest.raises(Exception) as exc_info:
        await service.sync_products()
    assert str(exc_info.value) == "Sync Error"


@pytest.mark.asyncio
async def test_sync_stock_success(service, mock_woo_service, mock_wolvox_service):
    """sync_stock başarılı durumu testi."""
    # Test verileri
    mock_products = [
        {
            "stokkodu": "TEST001",
            "stok_miktari": 10
        }
    ]
    
    # Mock ayarları
    mock_wolvox_service.get_products.return_value = mock_products
    mock_woo_service.update_stock.return_value = True
    
    # Test
    result = await service.sync_stock()
    
    # Doğrulamalar
    assert result is True
    mock_wolvox_service.get_products.assert_called_once()
    mock_woo_service.update_stock.assert_called_once_with("TEST001", 10)


@pytest.mark.asyncio
async def test_sync_stock_error(service, mock_wolvox_service):
    """sync_stock hata durumu testi."""
    # Mock ayarları
    mock_wolvox_service.get_products.side_effect = Exception("Stock Sync Error")
    
    # Test ve doğrulama
    with pytest.raises(Exception) as exc_info:
        await service.sync_stock()
    assert str(exc_info.value) == "Stock Sync Error"


@pytest.mark.asyncio
async def test_sync_orders_success(service, mock_woo_service, mock_wolvox_service):
    """sync_orders başarılı durumu testi."""
    # Test verileri
    mock_orders = [
        {
            "id": 1,
            "total": "100.00",
            "status": "processing"
        }
    ]
    
    # Mock ayarları
    mock_woo_service.get_new_orders.return_value = mock_orders
    mock_wolvox_service.create_order.return_value = True
    
    # Test
    result = await service.sync_orders()
    
    # Doğrulamalar
    assert result is True
    mock_woo_service.get_new_orders.assert_called_once()
    mock_wolvox_service.create_order.assert_called_once_with(mock_orders[0])


@pytest.mark.asyncio
async def test_sync_orders_error(service, mock_woo_service):
    """sync_orders hata durumu testi."""
    # Mock ayarları
    mock_woo_service.get_new_orders.side_effect = Exception("Order Sync Error")
    
    # Test ve doğrulama
    with pytest.raises(Exception) as exc_info:
        await service.sync_orders()
    assert str(exc_info.value) == "Order Sync Error" 
