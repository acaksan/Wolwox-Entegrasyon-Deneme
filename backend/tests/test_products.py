from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient
from main import app
from wolvox.wolvox_service import WolvoxService

client = TestClient(app)

@pytest.fixture
def mock_wolvox_service():
    with patch('wolvox.wolvox_service.WolvoxService') as mock:
        yield mock

def test_list_products(mock_wolvox_service):
    """Ürün listesi endpoint testi"""
    mock_products = [
        {
            "code": "PRD001",
            "name": "Test Ürün 1",
            "price": 100.0,
            "stock": 10
        }
    ]
    mock_wolvox_service.return_value.get_products.return_value = mock_products
    
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == mock_products

def test_sync_products(mock_wolvox_service):
    """Ürün senkronizasyonu endpoint testi"""
    mock_result = {
        "synced": 1,
        "failed": 0,
        "details": ["PRD001 senkronize edildi"]
    }
    mock_wolvox_service.return_value.sync_products.return_value = mock_result
    
    response = client.post("/api/v1/products/sync?limit=10")
    assert response.status_code == 200
    assert response.json() == mock_result 