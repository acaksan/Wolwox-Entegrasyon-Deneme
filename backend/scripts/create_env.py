import os

env_content = """
# WooCommerce Ayarları
WOOCOMMERCE_URL=https://lastik-al.com
WOOCOMMERCE_CONSUMER_KEY=ck_14ca8aab6f546bb34e5fd7f27ab0f77c6728c066
WOOCOMMERCE_CONSUMER_SECRET=cs_62e4007a181e06ed919fa469baaf6e3fac8ea45f
WOOCOMMERCE_VERSION=wc/v3
WOOCOMMERCE_TIMEOUT=30
WOOCOMMERCE_VERIFY_SSL=true
WOOCOMMERCE_QUERY_STRING_AUTH=true
""".strip()

with open(".env", "w", encoding="utf-8") as f:
    f.write(env_content)

print("✅ .env dosyası oluşturuldu") 