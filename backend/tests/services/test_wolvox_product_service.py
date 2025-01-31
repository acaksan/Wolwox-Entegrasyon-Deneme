"""WolvoxProductService testleri."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from services.wolvox_product_service import WolvoxProductService


@pytest.fixture
def mock_settings():
    """Test ayarları fixture'ı."""
    return Mock(
        FIREBIRD_HOST="localhost",
        FIREBIRD_DATABASE="test.fdb",
        FIREBIRD_USER="test",
        FIREBIRD_PASSWORD="test",
        FIREBIRD_PORT=3050,
        FIREBIRD_CHARSET="WIN1254"
    )


@pytest.fixture
def mock_db_connection():
    """Mock veritabanı bağlantısı fixture'ı."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.__enter__.return_value = mock_cursor
    return mock_conn


@pytest.fixture
def service(mock_settings):
    """WolvoxProductService fixture'ı."""
    with patch("services.wolvox_product_service.get_settings", return_value=mock_settings):
        service = WolvoxProductService()
        return service


@pytest.mark.asyncio
async def test_get_products_success(service, mock_db_connection):
    """get_products başarılı durumu testi."""
    # Test verileri
    mock_rows = [
        (1, "TEST001", "Test Ürün", "BARKOD001", "ADET", 18.0, "MARKA", "MODEL",
         "GRUP", "ALTGRUP", 1, 1, 1.5, "Açıklama", "resim.jpg", "Not 1", "Not 2",
         "Not 3", "Not 4", 10.0, 100.0)
    ]
    
    # Mock ayarları
    mock_cursor = mock_db_connection.cursor().__enter__()
    mock_cursor.fetchall.return_value = mock_rows
    
    with patch.object(service, "get_db_connection", return_value=mock_db_connection):
        # Test
        result = await service.get_products()
        
        # Doğrulamalar
        assert len(result) == 1
        product = result[0]
        assert product["blkodu"] == 1
        assert product["stokkodu"] == "TEST001"
        assert product["stok_adi"] == "Test Ürün"
        assert product["barkodu"] == "BARKOD001"
        assert product["birimi"] == "ADET"
        assert product["kdv_orani"] == 18.0
        assert product["markasi"] == "MARKA"
        assert product["modeli"] == "MODEL"
        assert product["grubu"] == "GRUP"
        assert product["alt_grubu"] == "ALTGRUP"
        assert product["webde_gorunsun"] is True
        assert product["aktif"] is True
        assert product["birim_agirlik"] == 1.5
        assert product["eticaret_aciklama"] == "Açıklama"
        assert product["resim_yolu"] == "resim.jpg"
        assert product["aciklama1"] == "Not 1"
        assert product["aciklama2"] == "Not 2"
        assert product["aciklama3"] == "Not 3"
        assert product["aciklama4"] == "Not 4"
        assert product["stok_miktari"] == 10.0
        assert product["satis_fiyati"] == 100.0


@pytest.mark.asyncio
async def test_get_products_empty(service, mock_db_connection):
    """get_products boş sonuç durumu testi."""
    # Mock ayarları
    mock_cursor = mock_db_connection.cursor().__enter__()
    mock_cursor.fetchall.return_value = []
    
    with patch.object(service, "get_db_connection", return_value=mock_db_connection):
        # Test
        result = await service.get_products()
        
        # Doğrulamalar
        assert len(result) == 0


@pytest.mark.asyncio
async def test_get_products_db_error(service):
    """get_products veritabanı hatası durumu testi."""
    # Mock ayarları
    with patch.object(service, "get_db_connection", side_effect=Exception("DB Error")):
        # Test ve doğrulama
        with pytest.raises(Exception) as exc_info:
            await service.get_products()
        assert str(exc_info.value) == "DB Error"


def test_get_db_connection_success(service):
    """get_db_connection başarılı durumu testi."""
    mock_conn = MagicMock()
    
    with patch("fdb.connect", return_value=mock_conn) as mock_connect:
        # Test
        result = service.get_db_connection()
        
        # Doğrulamalar
        assert result == mock_conn
        mock_connect.assert_called_once_with(
            host="localhost",
            database="test.fdb",
            user="test",
            password="test",
            port=3050,
            charset="WIN1254"
        )


def test_get_db_connection_error(service):
    """get_db_connection hata durumu testi."""
    with patch("fdb.connect", side_effect=Exception("Connection Error")):
        # Test ve doğrulama
        with pytest.raises(Exception) as exc_info:
            service.get_db_connection()
        assert str(exc_info.value) == "Connection Error" 