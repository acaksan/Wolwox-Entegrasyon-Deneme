"""WolvoxKasaService testleri."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from core.exceptions import DatabaseError
from services.wolvox_kasa_service import WolvoxKasaService


@pytest.fixture
def wolvox_kasa_service():
    """WolvoxKasaService fixture."""
    return WolvoxKasaService()


@pytest.mark.asyncio
async def test_get_kasa_listesi_success(wolvox_kasa_service):
    """get_kasa_listesi başarılı durumu testi."""
    # Mock data
    mock_kasa_listesi = [
        {
            "KASA_KODU": "KASA001",
            "KASA_ADI": "Ana Kasa",
            "DOVIZ_CINSI": "TL",
            "BAKIYE": 1000.00
        },
        {
            "KASA_KODU": "KASA002",
            "KASA_ADI": "Dolar Kasası",
            "DOVIZ_CINSI": "USD",
            "BAKIYE": 500.00
        }
    ]

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=mock_kasa_listesi)

    # Test
    result = await wolvox_kasa_service.get_kasa_listesi()

    # Assertions
    assert result == mock_kasa_listesi
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_listesi_error(wolvox_kasa_service):
    """get_kasa_listesi hata durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.get_kasa_listesi()

    assert str(exc_info.value) == "Kasa listesi alınırken hata: DB error"


@pytest.mark.asyncio
async def test_get_kasa_hareket_success(wolvox_kasa_service):
    """get_kasa_hareket başarılı durumu testi."""
    # Mock data
    mock_kasa_hareket = {
        "HAREKET_NO": 1,
        "KASA_KODU": "KASA001",
        "HAREKET_TIPI": "GIRIS",
        "TUTAR": 100.00,
        "TARIH": datetime.now(),
        "ACIKLAMA": "Test hareket"
    }

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=[mock_kasa_hareket])

    # Test
    result = await wolvox_kasa_service.get_kasa_hareket(1)

    # Assertions
    assert result == mock_kasa_hareket
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_hareket_not_found(wolvox_kasa_service):
    """get_kasa_hareket bulunamama durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=[])

    # Test
    result = await wolvox_kasa_service.get_kasa_hareket(999)

    # Assertions
    assert result is None
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_hareket_error(wolvox_kasa_service):
    """get_kasa_hareket hata durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.get_kasa_hareket(1)

    assert str(exc_info.value) == "Kasa hareketi alınırken hata: DB error"


@pytest.mark.asyncio
async def test_create_kasa_hareket_success(wolvox_kasa_service):
    """create_kasa_hareket başarılı durumu testi."""
    # Mock data
    mock_hareket_data = {
        "KASA_KODU": "KASA001",
        "HAREKET_TIPI": "GIRIS",
        "TUTAR": 100.00,
        "ACIKLAMA": "Test hareket"
    }

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_non_query = AsyncMock(return_value=True)

    # Test
    result = await wolvox_kasa_service.create_kasa_hareket(**mock_hareket_data)

    # Assertions
    assert result is True
    wolvox_kasa_service.db_pool.execute_non_query.assert_called_once()


@pytest.mark.asyncio
async def test_create_kasa_hareket_error(wolvox_kasa_service):
    """create_kasa_hareket hata durumu testi."""
    # Mock data
    mock_hareket_data = {
        "KASA_KODU": "KASA001",
        "HAREKET_TIPI": "GIRIS",
        "TUTAR": 100.00,
        "ACIKLAMA": "Test hareket"
    }

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_non_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.create_kasa_hareket(**mock_hareket_data)

    assert str(exc_info.value) == "Kasa hareketi oluşturulurken hata: DB error"


@pytest.mark.asyncio
async def test_get_kasa_bakiye_success(wolvox_kasa_service):
    """get_kasa_bakiye başarılı durumu testi."""
    # Mock data
    mock_bakiye = {
        "KASA_KODU": "KASA001",
        "BAKIYE": 1000.00,
        "DOVIZ_CINSI": "TL"
    }

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=[mock_bakiye])

    # Test
    result = await wolvox_kasa_service.get_kasa_bakiye("KASA001")

    # Assertions
    assert result == mock_bakiye
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_bakiye_error(wolvox_kasa_service):
    """get_kasa_bakiye hata durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.get_kasa_bakiye("KASA001")

    assert str(exc_info.value) == "Kasa bakiyesi alınırken hata: DB error"


@pytest.mark.asyncio
async def test_get_kasa_hareketleri_success(wolvox_kasa_service):
    """get_kasa_hareketleri başarılı durumu testi."""
    # Mock data
    mock_hareketler = [
        {
            "HAREKET_NO": 1,
            "KASA_KODU": "KASA001",
            "HAREKET_TIPI": "GIRIS",
            "TUTAR": 100.00,
            "TARIH": datetime.now(),
            "ACIKLAMA": "Test hareket 1"
        },
        {
            "HAREKET_NO": 2,
            "KASA_KODU": "KASA001",
            "HAREKET_TIPI": "CIKIS",
            "TUTAR": 50.00,
            "TARIH": datetime.now(),
            "ACIKLAMA": "Test hareket 2"
        }
    ]

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=mock_hareketler)

    # Test
    result = await wolvox_kasa_service.get_kasa_hareketleri(
        "KASA001",
        datetime.now(),
        datetime.now()
    )

    # Assertions
    assert result == mock_hareketler
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_hareketleri_error(wolvox_kasa_service):
    """get_kasa_hareketleri hata durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.get_kasa_hareketleri(
            "KASA001",
            datetime.now(),
            datetime.now()
        )

    assert str(exc_info.value) == "Kasa hareketleri alınırken hata: DB error"


@pytest.mark.asyncio
async def test_get_kasa_raporu_success(wolvox_kasa_service):
    """get_kasa_raporu başarılı durumu testi."""
    # Mock data
    mock_rapor = {
        "KASA_KODU": "KASA001",
        "BASLANGIC_BAKIYE": 1000.00,
        "TOPLAM_GIRIS": 500.00,
        "TOPLAM_CIKIS": 300.00,
        "BITIS_BAKIYE": 1200.00,
        "HAREKET_SAYISI": 10
    }

    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(return_value=[mock_rapor])

    # Test
    result = await wolvox_kasa_service.get_kasa_raporu(
        "KASA001",
        datetime.now(),
        datetime.now()
    )

    # Assertions
    assert result == mock_rapor
    wolvox_kasa_service.db_pool.execute_query.assert_called_once()


@pytest.mark.asyncio
async def test_get_kasa_raporu_error(wolvox_kasa_service):
    """get_kasa_raporu hata durumu testi."""
    # Mock DatabasePool
    wolvox_kasa_service.db_pool.execute_query = AsyncMock(side_effect=Exception("DB error"))

    # Test
    with pytest.raises(DatabaseError) as exc_info:
        await wolvox_kasa_service.get_kasa_raporu(
            "KASA001",
            datetime.now(),
            datetime.now()
        )

    assert str(exc_info.value) == "Kasa raporu alınırken hata: DB error" 