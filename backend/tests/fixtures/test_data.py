"""Test verileri."""

from datetime import datetime

# Mock Cari Verileri
MOCK_CARI = {
    'BLKODU': 1,
    'CARIKODU': 'C001',
    'UNVAN1': 'Test Müşteri',
    'UNVAN2': None,
    'VERGIDAIRESI': 'Test VD',
    'VERGINO': '1234567890',
    'TCKIMLIKNO': None,
    'TELEFON1': '5551234567',
    'TELEFON2': None,
    'EMAIL': 'test@test.com',
    'IL': 'İSTANBUL',
    'ILCE': 'KADIKÖY',
    'ADRES1': 'Test Adres 1',
    'ADRES2': None,
    'AKTIF': 1,
    'WEBDE_GORUNSUN': 1
}

# Mock Stok Verileri
MOCK_STOK = {
    'BLKODU': 1,
    'STOKKODU': 'S001',
    'STOK_ADI': 'Test Ürün',
    'BARKODU': '8680001234567',
    'BIRIM': 'ADET',
    'AKTIF': 1,
    'WEBDE_GORUNSUN': 1,
    'STOK_MIKTARI': 100,
    'SATIS_FIYATI': 100.0,
    'ALIS_FIYATI': 80.0
}

MOCK_STOK_HAREKET = {
    'BLKODU': 1,
    'EVRAK_NO': 'STH20240301001',
    'EVRAK_TIPI': 'FAT',
    'GIRIS_CIKIS': 'G',
    'MIKTAR': 10,
    'BIRIM_FIYAT': 100.0,
    'TUTAR': 1000.0,
    'TARIH': datetime(2024, 3, 1)
}

MOCK_STOK_FIYAT = {
    'BLKODU': 1,
    'BLSTKODU': 1,
    'FIYATI': 150.0,
    'TARIH': datetime(2024, 3, 1),
    'ACIKLAMA': 'Test fiyat kaydı'
}

# Mock Sipariş Verileri
MOCK_SIPARIS = {
    'BLKODU': 1,
    'SIPARIS_NO': 'SIP20240301001',
    'TARIH': datetime(2024, 3, 1),
    'CARI_BLKODU': 1,
    'TOPLAM_TUTAR': 1000.0,
    'KDV_TOPLAMI': 180.0,
    'GENEL_TOPLAM': 1180.0,
    'ACIKLAMA': 'Test sipariş',
    'DURUM': 'B'
}

MOCK_SIPARIS_DETAY = {
    'BLKODU': 1,
    'BLSIPKODU': 1,
    'BLSTKODU': 1,
    'MIKTAR': 10,
    'BIRIM_FIYAT': 100.0,
    'KDV_ORANI': 18,
    'TUTAR': 1000.0,
    'KDV_TUTARI': 180.0,
    'TOPLAM_TUTAR': 1180.0
}

# Mock Fatura Verileri
MOCK_FATURA = {
    'BLKODU': 1,
    'FATURA_NO': 'SF20240301001',
    'FATURA_TIPI': 'S',
    'TARIH': datetime(2024, 3, 1),
    'CARI_BLKODU': 1,
    'TOPLAM_TUTAR': 1000.0,
    'KDV_TOPLAMI': 180.0,
    'GENEL_TOPLAM': 1180.0,
    'ACIKLAMA': 'Test fatura',
    'DURUM': 'A'
}

MOCK_FATURA_DETAY = {
    'BLKODU': 1,
    'BLFATKODU': 1,
    'BLSTKODU': 1,
    'MIKTAR': 10,
    'BIRIM_FIYAT': 100.0,
    'KDV_ORANI': 18,
    'TUTAR': 1000.0,
    'KDV_TUTARI': 180.0,
    'TOPLAM_TUTAR': 1180.0
}

# Mock Kasa Verileri
MOCK_KASA = {
    'BLKODU': 1,
    'KASA_KODU': 'K001',
    'KASA_ADI': 'Test Kasa',
    'AKTIF': 1,
    'BAKIYE': 5000.0
}

MOCK_KASA_HAREKET = {
    'BLKODU': 1,
    'EVRAK_NO': 'NAK20240301001',
    'EVRAK_TIPI': 'NAK',
    'GIRIS_CIKIS': 'G',
    'TUTAR': 1000.0,
    'TARIH': datetime(2024, 3, 1),
    'ACIKLAMA': 'Test tahsilat'
}

# Mock Banka Verileri
MOCK_BANKA = {
    'BLKODU': 1,
    'BANKA_KODU': 'B001',
    'BANKA_ADI': 'Test Banka',
    'SUBE_ADI': 'Test Şube',
    'HESAP_NO': '123456789',
    'IBAN': 'TR123456789012345678901234',
    'AKTIF': 1,
    'BAKIYE': 10000.0
}

MOCK_BANKA_HAREKET = {
    'BLKODU': 1,
    'EVRAK_NO': 'HAV20240301001',
    'EVRAK_TIPI': 'HAV',
    'GIRIS_CIKIS': 'G',
    'TUTAR': 1000.0,
    'TARIH': datetime(2024, 3, 1),
    'ACIKLAMA': 'Test havale'
}

# Mock İstatistik Verileri
MOCK_REVENUE_STATS = {
    'total_revenue': 50000.0,
    'total_orders': 100,
    'average_order_value': 500.0,
    'total_customers': 50,
    'top_products': [
        {'product_name': 'Ürün 1', 'total_sales': 10000.0},
        {'product_name': 'Ürün 2', 'total_sales': 8000.0},
        {'product_name': 'Ürün 3', 'total_sales': 6000.0}
    ],
    'revenue_by_month': {
        '2024-01': 15000.0,
        '2024-02': 17000.0,
        '2024-03': 18000.0
    }
}

MOCK_INVENTORY_STATS = {
    'total_products': 1000,
    'total_value': 100000.0,
    'low_stock_items': 50,
    'out_of_stock_items': 10,
    'top_categories': [
        {'category_name': 'Kategori 1', 'product_count': 300},
        {'category_name': 'Kategori 2', 'product_count': 250},
        {'category_name': 'Kategori 3', 'product_count': 200}
    ],
    'stock_movements': {
        '2024-01': {'in': 1000, 'out': 800},
        '2024-02': {'in': 1200, 'out': 900},
        '2024-03': {'in': 1100, 'out': 950}
    }
}

MOCK_CUSTOMER_STATS = {
    'total_customers': 500,
    'active_customers': 300,
    'new_customers': 50,
    'customer_segments': {
        'VIP': 50,
        'Regular': 200,
        'Occasional': 250
    },
    'top_customers': [
        {'customer_name': 'Müşteri 1', 'total_purchases': 20000.0},
        {'customer_name': 'Müşteri 2', 'total_purchases': 15000.0},
        {'customer_name': 'Müşteri 3', 'total_purchases': 12000.0}
    ],
    'customer_growth': {
        '2024-01': 20,
        '2024-02': 15,
        '2024-03': 15
    }
}

MOCK_FINANCIAL_STATS = {
    'total_revenue': 500000.0,
    'total_expenses': 300000.0,
    'net_profit': 200000.0,
    'accounts_receivable': 50000.0,
    'accounts_payable': 30000.0,
    'cash_flow': {
        '2024-01': {'in': 100000.0, 'out': 60000.0},
        '2024-02': {'in': 110000.0, 'out': 65000.0},
        '2024-03': {'in': 120000.0, 'out': 70000.0}
    },
    'profit_margins': {
        'gross': 0.4,
        'net': 0.25,
        'operating': 0.3
    }
} 