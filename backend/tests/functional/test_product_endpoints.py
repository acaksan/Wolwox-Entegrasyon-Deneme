"""Ürün endpoint testleri"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.api.schemas.product import ProductCreate
from src.api.v1.woocommerce.woocommerce_service import wc_service
from src.main import app
from src.wolvox.wolvox_service import wolvox_service

client = TestClient(app)

@pytest.fixture
def mock_wc_service():
    with patch('src.api.v1.woocommerce.woocommerce_service.wc_service') as mock:
        yield mock

@pytest.fixture
def mock_wolvox_service():
    with patch('src.wolvox.wolvox_service.wolvox_service') as mock:
        yield mock

def test_create_product(client: TestClient, db: Session):
    """
    Ürün oluşturma endpoint'ini test eder
    """
    product_data = {
        "name": "Test Ürün",
        "description": "Test açıklama",
        "price": 100.0,
        "stock_quantity": 10,
        "wolvox_id": "TEST001",
        "wolvox_code": "TEST-001",
        "wolvox_barcode": "1234567890"
    }
    
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["wolvox_id"] == product_data["wolvox_id"]
    assert "id" in data

def test_get_product(client: TestClient, db: Session):
    """
    Ürün getirme endpoint'ini test eder
    """
    # Önce test ürünü oluştur
    product_data = {
        "name": "Test Ürün",
        "description": "Test açıklama",
        "price": 100.0,
        "stock_quantity": 10,
        "wolvox_id": "TEST001",
        "wolvox_code": "TEST-001",
        "wolvox_barcode": "1234567890"
    }
    
    create_response = client.post("/api/v1/products/", json=product_data)
    created_product = create_response.json()
    
    # Oluşturulan ürünü getir
    response = client.get(f"/api/v1/products/{created_product['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["wolvox_id"] == product_data["wolvox_id"]

def test_get_product_by_wolvox_id(client: TestClient, db: Session):
    """
    Wolvox ID ile ürün getirme endpoint'ini test eder
    """
    # Önce test ürünü oluştur
    product_data = {
        "name": "Test Ürün",
        "description": "Test açıklama",
        "price": 100.0,
        "stock_quantity": 10,
        "wolvox_id": "TEST001",
        "wolvox_code": "TEST-001",
        "wolvox_barcode": "1234567890"
    }
    
    client.post("/api/v1/products/", json=product_data)
    
    # Wolvox ID ile ürünü getir
    response = client.get(f"/api/v1/products/wolvox/{product_data['wolvox_id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["wolvox_id"] == product_data["wolvox_id"]

def test_update_product(client: TestClient, db: Session):
    """
    Ürün güncelleme endpoint'ini test eder
    """
    # Önce test ürünü oluştur
    product_data = {
        "name": "Test Ürün",
        "description": "Test açıklama",
        "price": 100.0,
        "stock_quantity": 10,
        "wolvox_id": "TEST001",
        "wolvox_code": "TEST-001",
        "wolvox_barcode": "1234567890"
    }
    
    create_response = client.post("/api/v1/products/", json=product_data)
    created_product = create_response.json()
    
    # Ürünü güncelle
    update_data = {
        "name": "Güncellenmiş Ürün",
        "price": 150.0
    }
    
    response = client.put(f"/api/v1/products/{created_product['id']}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]
    assert data["wolvox_id"] == product_data["wolvox_id"]

def test_delete_product(client: TestClient, db: Session):
    """
    Ürün silme endpoint'ini test eder
    """
    # Önce test ürünü oluştur
    product_data = {
        "name": "Test Ürün",
        "description": "Test açıklama",
        "price": 100.0,
        "stock_quantity": 10,
        "wolvox_id": "TEST001",
        "wolvox_code": "TEST-001",
        "wolvox_barcode": "1234567890"
    }
    
    create_response = client.post("/api/v1/products/", json=product_data)
    created_product = create_response.json()
    
    # Ürünü sil
    response = client.delete(f"/api/v1/products/{created_product['id']}")
    assert response.status_code == 200
    
    # Silinen ürünü getirmeyi dene
    get_response = client.get(f"/api/v1/products/{created_product['id']}")
    assert get_response.status_code == 404

def test_get_wc_products(mock_wc_service):
    """WooCommerce ürün listesi endpoint testi"""
    mock_products = [
        {"id": 1, "name": "Test Product 1"},
        {"id": 2, "name": "Test Product 2"}
    ]
    mock_wc_service.get_products.return_value = mock_products

    response = client.get("/api/v1/woocommerce/products")
    assert response.status_code == 200
    assert response.json() == mock_products

def test_get_wc_product(mock_wc_service):
    """WooCommerce ürün detay endpoint testi"""
    mock_product = {"id": 1, "name": "Test Product"}
    mock_wc_service.get_product.return_value = mock_product

    response = client.get("/api/v1/woocommerce/products/1")
    assert response.status_code == 200
    assert response.json() == mock_product

def test_get_wolvox_products(mock_wolvox_service):
    """Wolvox ürün listesi endpoint testi"""
    mock_products = [
        {"stok_kodu": "P1", "stok_adi": "Test Product 1"},
        {"stok_kodu": "P2", "stok_adi": "Test Product 2"}
    ]
    mock_wolvox_service.get_products.return_value = mock_products

    response = client.get("/api/v1/wolvox/products")
    assert response.status_code == 200
    assert response.json() == mock_products

def test_get_wolvox_product(mock_wolvox_service):
    """Wolvox ürün detay endpoint testi"""
    mock_product = {"stok_kodu": "P1", "stok_adi": "Test Product"}
    mock_wolvox_service.get_product.return_value = mock_product

    response = client.get("/api/v1/wolvox/products/P1")
    assert response.status_code == 200
    assert response.json() == mock_product

def test_sync_product(mock_wc_service, mock_wolvox_service):
    """Ürün senkronizasyon endpoint testi"""
    mock_wolvox_product = {
        "stok_kodu": "P1",
        "stok_adi": "Test Product",
        "satis_fiyat1": 100.0,
        "kdv_orani": 18
    }
    mock_wc_product = {
        "id": 1,
        "name": "Test Product",
        "regular_price": "118.0",
        "tax_class": "standard"
    }

    mock_wolvox_service.get_product.return_value = mock_wolvox_product
    mock_wc_service.update_product.return_value = mock_wc_product

    response = client.post("/api/v1/sync/products/P1")
    assert response.status_code == 200
    assert response.json() == {
        "wolvox_product": mock_wolvox_product,
        "wc_product": mock_wc_product
    } 