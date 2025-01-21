import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Firebird veritabanı ayarları
FB_HOST = 'localhost'
FB_DATABASE = r'D:\AKINSOFT\Wolvox8\Database_FB\DEMOWOLVOX\2025\WOLVOX.FDB'
FB_USER = 'SYSDBA'
FB_PASSWORD = 'masterkey'
FB_CHARSET = 'WIN1254'
FB_PORT = 3050

# WooCommerce API ayarları
WC_URL = 'https://lastik-al.com'
WC_CONSUMER_KEY = 'ck_14ca8aab6f546bb34e5fd7f27ab0f77c6728c066'
WC_CONSUMER_SECRET = 'cs_62e4007a181e06ed919fa469baaf6e3fac8ea45f'
WC_VERSION = 'wc/v3'

# Debug modu
DEBUG = True
