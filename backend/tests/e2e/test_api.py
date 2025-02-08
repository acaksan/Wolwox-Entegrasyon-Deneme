from datetime import datetime

import pytest
from core.security import create_test_token
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app


@pytest.mark.e2e
class TestAPI:
    @pytest.fixture
    async def client(self):
        """Test client with authentication."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test token oluştur
            token = create_test_token()
            client.headers["Authorization"] = f"Bearer {token}"
            yield client
    
    @pytest.fixture
    def test_product(self):
        """Test ürün verisi."""
        return {
            "sku": f"TEST{datetime.now().timestamp()}",
            "name": "Test Product",
            "regular_price": "99.90",
            "stock_quantity": 100,
            "manage_stock": True
        }

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
    @pytest.mark.asyncio
    async def test_product_crud(self, client, test_product):
        """Test product CRUD operations."""
        # Create
        response = await client.post("/api/v1/products", json=test_product)
        assert response.status_code == 201
        product_id = response.json()["id"]
        
        # Read
        response = await client.get(f"/api/v1/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["sku"] == test_product["sku"]
        
        # Update
        update_data = {"regular_price": "149.90"}
        response = await client.patch(
            f"/api/v1/products/{product_id}",
            json=update_data
        )
        assert response.status_code == 200
        assert response.json()["regular_price"] == update_data["regular_price"]
        
        # Delete
        response = await client.delete(f"/api/v1/products/{product_id}")
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_product_validation(self, client):
        """Test product validation."""
        invalid_products = [
            # Boş SKU
            {
                "sku": "",
                "name": "Test Product",
                "regular_price": "99.90"
            },
            # Negatif fiyat
            {
                "sku": "TEST1",
                "name": "Test Product",
                "regular_price": "-99.90"
            },
            # Negatif stok
            {
                "sku": "TEST2",
                "name": "Test Product",
                "regular_price": "99.90",
                "stock_quantity": -10
            }
        ]
        
        for product in invalid_products:
            response = await client.post("/api/v1/products", json=product)
            assert response.status_code == 422
            assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_product_search(self, client, test_product):
        """Test product search functionality."""
        # Create test product
        response = await client.post("/api/v1/products", json=test_product)
        assert response.status_code == 201
        
        # Search by SKU
        response = await client.get(
            "/api/v1/products/search",
            params={"sku": test_product["sku"]}
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) == 1
        
        # Search by name
        response = await client.get(
            "/api/v1/products/search",
            params={"name": "Test"}
        )
        assert response.status_code == 200
        assert len(response.json()["items"]) >= 1

    @pytest.mark.asyncio
    async def test_sync_endpoints(self, client):
        """Test sync related endpoints."""
        # Manual sync trigger
        response = await client.post(
            "/api/v1/sync/products",
            params={"force": True}
        )
        assert response.status_code == 202
        job_id = response.json()["job_id"]
        
        # Check sync status
        response = await client.get(f"/api/v1/sync/status/{job_id}")
        assert response.status_code == 200
        assert response.json()["status"] in ["pending", "in_progress", "completed"]

    @pytest.mark.asyncio
    async def test_bulk_operations(self, client):
        """Test bulk operations."""
        # Bulk create
        products = [
            {
                "sku": f"BULK{i}",
                "name": f"Bulk Product {i}",
                "regular_price": "99.90",
                "stock_quantity": 100
            }
            for i in range(3)
        ]
        
        response = await client.post("/api/v1/products/bulk", json=products)
        assert response.status_code == 201
        product_ids = response.json()["ids"]
        
        # Bulk update
        updates = [
            {"id": id, "stock_quantity": 50}
            for id in product_ids
        ]
        response = await client.put("/api/v1/products/bulk", json=updates)
        assert response.status_code == 200
        
        # Bulk delete
        response = await client.delete(
            "/api/v1/products/bulk",
            json={"ids": product_ids}
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_error_handling(self, client):
        """Test API error handling."""
        # 404 Not Found
        response = await client.get("/api/v1/products/99999")
        assert response.status_code == 404
        
        # 400 Bad Request
        response = await client.post(
            "/api/v1/sync/products",
            json={"invalid": "data"}
        )
        assert response.status_code == 400
        
        # 401 Unauthorized
        async with AsyncClient(app=app, base_url="http://test") as unauth_client:
            response = await unauth_client.get("/api/v1/products")
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_pagination(self, client):
        """Test pagination functionality."""
        # Get first page
        response = await client.get(
            "/api/v1/products",
            params={"page": 1, "per_page": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        
        # Verify next page
        if data["total"] > 10:
            response = await client.get(
                "/api/v1/products",
                params={"page": 2, "per_page": 10}
            )
            assert response.status_code == 200
            assert response.json()["page"] == 2

    def test_upload_image(self, client):
        files = {
            'file': ('test.jpg', open('tests/fixtures/test_image.jpg', 'rb'))
        }
        data = {'title': 'Test Upload'}
        
        response = client.post("/api/upload", files=files, data=data)
        assert response.status_code == 200
        assert response.json()["title"] == "Test Upload" 