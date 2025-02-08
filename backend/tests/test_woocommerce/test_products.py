import pytest
from fastapi.testclient import TestClient


@pytest.mark.woo
def test_get_products(test_client: TestClient):
    response = test_client.get("/api/v1/products")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "success"

@pytest.mark.woo
def test_sync_products(test_client: TestClient):
    response = test_client.post("/api/v1/products/sync")
    assert response.status_code == 202
    assert response.json()["status"] == "success"

@pytest.mark.woo
def test_create_product(test_client: TestClient, woo_test_data):
    response = test_client.post(
        "/api/v1/products",
        json=woo_test_data["product"]
    )
    
    # Response'un JSON olduğunu kontrol et
    response_data = response.json()
    
    # Başarılı durum
    if response.status_code == 201:
        assert response_data["status"] == "success"
        assert "data" in response_data
        assert "message" in response_data
        assert response_data["message"] == "Ürün başarıyla oluşturuldu"
    
    # Hata durumu
    elif response.status_code == 400:
        assert response_data["status"] == "error"
        assert "detail" in response_data
        assert isinstance(response_data["detail"], str)
    
    # Diğer durumlarda hata ver
    else:
        pytest.fail(f"Beklenmeyen durum kodu: {response.status_code}") 