"""WooCommerce servis testleri"""

from unittest.mock import MagicMock, patch

import pytest
from src.api.v1.woocommerce.woocommerce_service import (WooCommerceService,
                                                        wc_service)
from src.core.exceptions import APIException


@pytest.fixture
def mock_wc_api():
    with patch('src.api.v1.woocommerce.woocommerce_service.API') as mock:
        yield mock

@pytest.fixture
def mock_cache():
    with patch('src.api.v1.woocommerce.woocommerce_service.cache') as mock:
        yield mock

def test_singleton_instance():
    """Singleton pattern test"""
    service1 = WooCommerceService()
    service2 = WooCommerceService()
    assert service1 is service2
    assert service1 is wc_service

@pytest.mark.asyncio
async def test_test_connection_success(mock_wc_api):
    """Bağlantı testi başarılı"""
    mock_wc_api.return_value.get.return_value = MagicMock()
    result = await wc_service.test_connection()
    assert result is True

@pytest.mark.asyncio
async def test_test_connection_failure(mock_wc_api):
    """Bağlantı testi başarısız"""
    mock_wc_api.return_value.get.side_effect = Exception("Connection error")
    result = await wc_service.test_connection()
    assert result is False

@pytest.mark.asyncio
async def test_get_products_success(mock_wc_api, mock_cache):
    """Ürün listesi başarıyla alındı"""
    mock_cache.get.return_value = None
    mock_products = [{"id": 1, "name": "Test Product"}]
    mock_wc_api.return_value.get.return_value.json.return_value = mock_products
    
    result = await wc_service.get_products(per_page=10)
    assert result == mock_products
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_products_from_cache(mock_wc_api, mock_cache):
    """Ürün listesi cache'den alındı"""
    mock_products = [{"id": 1, "name": "Test Product"}]
    mock_cache.get.return_value = mock_products
    
    result = await wc_service.get_products(per_page=10)
    assert result == mock_products
    mock_wc_api.return_value.get.assert_not_called()

@pytest.mark.asyncio
async def test_get_products_failure(mock_wc_api, mock_cache):
    """Ürün listesi alınamadı"""
    mock_cache.get.return_value = None
    mock_wc_api.return_value.get.side_effect = Exception("API error")
    
    with pytest.raises(APIException):
        await wc_service.get_products(per_page=10)

@pytest.mark.asyncio
async def test_get_product_success(mock_wc_api, mock_cache):
    """Ürün detayı başarıyla alındı"""
    mock_cache.get.return_value = None
    mock_product = {"id": 1, "name": "Test Product"}
    mock_wc_api.return_value.get.return_value.json.return_value = mock_product
    
    result = await wc_service.get_product(1)
    assert result == mock_product
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_product_from_cache(mock_wc_api, mock_cache):
    """Ürün detayı cache'den alındı"""
    mock_product = {"id": 1, "name": "Test Product"}
    mock_cache.get.return_value = mock_product
    
    result = await wc_service.get_product(1)
    assert result == mock_product
    mock_wc_api.return_value.get.assert_not_called()

@pytest.mark.asyncio
async def test_get_product_failure(mock_wc_api, mock_cache):
    """Ürün detayı alınamadı"""
    mock_cache.get.return_value = None
    mock_wc_api.return_value.get.side_effect = Exception("API error")
    
    with pytest.raises(APIException):
        await wc_service.get_product(1)

def test_create_product(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1, "name": "Yeni Ürün"}
    wc_service.wcapi.post.return_value = mock_response

    # Test data
    product_data = {"name": "Yeni Ürün", "regular_price": "99.99"}
    
    # Test
    result = wc_service.create_product(product_data)
    
    # Assertions
    assert result["name"] == "Yeni Ürün"
    wc_service.wcapi.post.assert_called_once_with("products", product_data)

def test_update_product(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Güncellenmiş Ürün"}
    wc_service.wcapi.put.return_value = mock_response

    # Test data
    product_data = {"name": "Güncellenmiş Ürün"}
    
    # Test
    result = wc_service.update_product(1, product_data)
    
    # Assertions
    assert result["name"] == "Güncellenmiş Ürün"
    wc_service.wcapi.put.assert_called_once_with("products/1", product_data)

def test_delete_product(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    wc_service.wcapi.delete.return_value = mock_response

    # Test
    result = wc_service.delete_product(1)
    
    # Assertions
    assert result is True
    wc_service.wcapi.delete.assert_called_once_with("products/1", params={"force": False})

def test_update_stock(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "stock_quantity": 10}
    wc_service.wcapi.put.return_value = mock_response

    # Test
    result = wc_service.update_stock(1, 10)
    
    # Assertions
    assert result["stock_quantity"] == 10
    wc_service.wcapi.put.assert_called_once_with("products/1", {
        "stock_quantity": 10,
        "manage_stock": True
    })

def test_get_orders(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "status": "processing"},
        {"id": 2, "status": "completed"}
    ]
    wc_service.wcapi.get.return_value = mock_response

    # Test
    orders = wc_service.get_orders(status="processing")
    
    # Assertions
    assert len(orders) == 2
    assert orders[0]["status"] == "processing"
    wc_service.wcapi.get.assert_called_once_with("orders", params={
        "page": 1,
        "per_page": 100,
        "status": "processing"
    })

def test_update_order_status(wc_service):
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "status": "completed"}
    wc_service.wcapi.put.return_value = mock_response

    # Test
    result = wc_service.update_order_status(1, "completed")
    
    # Assertions
    assert result["status"] == "completed"
    wc_service.wcapi.put.assert_called_once_with("orders/1", {"status": "completed"}) 