"""WooCommerceProductService testleri."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from core.exceptions import ServiceError
from services.woocommerce_product_service import WooCommerceProductService


@pytest.fixture
def woo_product_service():
    """WooCommerceProductService fixture."""
    return WooCommerceProductService()


@pytest.mark.asyncio
async def test_get_products_success(woo_product_service):
    """get_products başarılı durumu testi."""
    # Mock data
    mock_products = [
        {
            "id": 1,
            "name": "Test Ürün 1",
            "type": "simple",
            "status": "publish"
        },
        {
            "id": 2,
            "name": "Test Ürün 2",
            "type": "simple",
            "status": "publish"
        }
    ]

    # Mock WooCommerceService
    woo_product_service.woo_service.get = AsyncMock(return_value=mock_products)

    # Test
    result = await woo_product_service.get_products()

    # Assertions
    assert result == mock_products
    woo_product_service.woo_service.get.assert_called_once_with(
        "products",
        params={"page": 1, "per_page": 10, "status": "publish"}
    )


@pytest.mark.asyncio
async def test_get_products_error(woo_product_service):
    """get_products hata durumu testi."""
    # Mock WooCommerceService
    woo_product_service.woo_service.get = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.get_products()

    assert str(exc_info.value) == "Ürünler alınırken hata: API error"


@pytest.mark.asyncio
async def test_get_product_success(woo_product_service):
    """get_product başarılı durumu testi."""
    # Mock data
    mock_product = {
        "id": 1,
        "name": "Test Ürün",
        "type": "simple",
        "status": "publish"
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.get = AsyncMock(return_value=mock_product)

    # Test
    result = await woo_product_service.get_product(1)

    # Assertions
    assert result == mock_product
    woo_product_service.woo_service.get.assert_called_once_with("products/1")


@pytest.mark.asyncio
async def test_get_product_error(woo_product_service):
    """get_product hata durumu testi."""
    # Mock WooCommerceService
    woo_product_service.woo_service.get = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.get_product(1)

    assert str(exc_info.value) == "Ürün detayları alınırken hata: API error"


@pytest.mark.asyncio
async def test_create_product_success(woo_product_service):
    """create_product başarılı durumu testi."""
    # Mock data
    mock_product_data = {
        "name": "Test Ürün",
        "type": "simple",
        "regular_price": "10.00"
    }
    mock_response = {
        "id": 1,
        **mock_product_data
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.post = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.create_product(mock_product_data)

    # Assertions
    assert result == mock_response
    woo_product_service.woo_service.post.assert_called_once_with(
        "products",
        data=mock_product_data
    )


@pytest.mark.asyncio
async def test_create_product_error(woo_product_service):
    """create_product hata durumu testi."""
    # Mock data
    mock_product_data = {
        "name": "Test Ürün",
        "type": "simple",
        "regular_price": "10.00"
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.post = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.create_product(mock_product_data)

    assert str(exc_info.value) == "Ürün oluşturulurken hata: API error"


@pytest.mark.asyncio
async def test_update_product_success(woo_product_service):
    """update_product başarılı durumu testi."""
    # Mock data
    mock_product_data = {
        "name": "Test Ürün (Güncel)",
        "regular_price": "15.00"
    }
    mock_response = {
        "id": 1,
        **mock_product_data
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.put = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.update_product(1, mock_product_data)

    # Assertions
    assert result == mock_response
    woo_product_service.woo_service.put.assert_called_once_with(
        "products/1",
        data=mock_product_data
    )


@pytest.mark.asyncio
async def test_update_product_error(woo_product_service):
    """update_product hata durumu testi."""
    # Mock data
    mock_product_data = {
        "name": "Test Ürün (Güncel)",
        "regular_price": "15.00"
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.put = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.update_product(1, mock_product_data)

    assert str(exc_info.value) == "Ürün güncellenirken hata: API error"


@pytest.mark.asyncio
async def test_delete_product_success(woo_product_service):
    """delete_product başarılı durumu testi."""
    # Mock data
    mock_response = {
        "id": 1,
        "status": "trash"
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.delete = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.delete_product(1)

    # Assertions
    assert result == mock_response
    woo_product_service.woo_service.delete.assert_called_once_with(
        "products/1",
        params={"force": False}
    )


@pytest.mark.asyncio
async def test_delete_product_error(woo_product_service):
    """delete_product hata durumu testi."""
    # Mock WooCommerceService
    woo_product_service.woo_service.delete = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.delete_product(1)

    assert str(exc_info.value) == "Ürün silinirken hata: API error"


@pytest.mark.asyncio
async def test_update_stock_success(woo_product_service):
    """update_stock başarılı durumu testi."""
    # Mock data
    mock_response = {
        "id": 1,
        "stock_quantity": 10,
        "manage_stock": True
    }

    # Mock update_product method
    woo_product_service.update_product = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.update_stock(1, 10)

    # Assertions
    assert result == mock_response
    woo_product_service.update_product.assert_called_once_with(
        1,
        {"stock_quantity": 10, "manage_stock": True}
    )


@pytest.mark.asyncio
async def test_update_stock_error(woo_product_service):
    """update_stock hata durumu testi."""
    # Mock update_product method
    woo_product_service.update_product = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.update_stock(1, 10)

    assert str(exc_info.value) == "Stok güncellenirken hata: API error"


@pytest.mark.asyncio
async def test_update_price_success(woo_product_service):
    """update_price başarılı durumu testi."""
    # Mock data
    mock_response = {
        "id": 1,
        "regular_price": "20.00",
        "sale_price": "15.00"
    }

    # Mock update_product method
    woo_product_service.update_product = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.update_price(1, 20.00, 15.00)

    # Assertions
    assert result == mock_response
    woo_product_service.update_product.assert_called_once_with(
        1,
        {"regular_price": "20.00", "sale_price": "15.00"}
    )


@pytest.mark.asyncio
async def test_update_price_error(woo_product_service):
    """update_price hata durumu testi."""
    # Mock update_product method
    woo_product_service.update_product = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.update_price(1, 20.00, 15.00)

    assert str(exc_info.value) == "Fiyat güncellenirken hata: API error"


@pytest.mark.asyncio
async def test_batch_update_success(woo_product_service):
    """batch_update başarılı durumu testi."""
    # Mock data
    mock_products = [
        {"id": 1, "name": "Ürün 1"},
        {"id": 2, "name": "Ürün 2"}
    ]
    mock_response = {
        "update": [
            {"id": 1, "name": "Ürün 1"},
            {"id": 2, "name": "Ürün 2"}
        ]
    }

    # Mock WooCommerceService
    woo_product_service.woo_service.post = AsyncMock(return_value=mock_response)

    # Test
    result = await woo_product_service.batch_update(mock_products)

    # Assertions
    assert result == mock_response
    woo_product_service.woo_service.post.assert_called_once_with(
        "products/batch",
        data={"update": mock_products}
    )


@pytest.mark.asyncio
async def test_batch_update_error(woo_product_service):
    """batch_update hata durumu testi."""
    # Mock data
    mock_products = [
        {"id": 1, "name": "Ürün 1"},
        {"id": 2, "name": "Ürün 2"}
    ]

    # Mock WooCommerceService
    woo_product_service.woo_service.post = AsyncMock(side_effect=Exception("API error"))

    # Test
    with pytest.raises(ServiceError) as exc_info:
        await woo_product_service.batch_update(mock_products)

    assert str(exc_info.value) == "Toplu güncelleme yapılırken hata: API error" 