# Wolvox Entegrasyon

Wolvox Hotel yazılımı ile WooCommerce entegrasyonu için geliştirilmiş web uygulaması.

## Teknolojiler

- Frontend: React.js 18
- Backend: Node.js & Express.js
- Veritabanı: Firebird
- API: WooCommerce REST API

## Gereksinimler

- Node.js 16 veya üzeri
- Firebird 2.5
- WooCommerce kurulu WordPress sitesi

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/acaksan/Wolwox-Entegrasyon-Deneme.git
cd Wolwox-Entegrasyon-Deneme
```

2. Bağımlılıkları yükleyin:
```bash
npm install
```

3. `.env` dosyasını oluşturun ve gerekli ayarları yapın:
```env
# Firebird Ayarları
FIREBIRD_HOST=localhost
FIREBIRD_PORT=3050
FIREBIRD_DATABASE=C:\\path\\to\\database.fdb
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=masterkey
FIREBIRD_PAGE_SIZE=4096
FIREBIRD_RETRY_INTERVAL=1000
FIREBIRD_POOL_SIZE=5
FIREBIRD_CHARSET=WIN1254
FIREBIRD_CLIENT_LIBRARY=C:\\Program Files (x86)\\Firebird\\Firebird_2_5\\bin\\fbclient.dll

# WooCommerce Ayarları
WOOCOMMERCE_URL=https://your-site.com
WOOCOMMERCE_CONSUMER_KEY=your_consumer_key
WOOCOMMERCE_CONSUMER_SECRET=your_consumer_secret

# Server Ayarları
PORT=3002
NODE_ENV=development
```

4. Uygulamayı başlatın:
```bash
npm run dev
```

Frontend: http://localhost:3000
Backend: http://localhost:3002

## Özellikler

- Firebird veritabanı bağlantısı ve sorgu yönetimi
- WooCommerce ürün senkronizasyonu
- Stok takibi
- Fiyat güncelleme
- Sipariş yönetimi

## Notlar

- Firebird veritabanı bağlantısı için fbclient.dll dosyasının sistemde kurulu olması gerekir
- WooCommerce API anahtarlarının doğru yapılandırılması gerekir
- Node.js'in PATH'e eklenmiş olması gerekir

## Hata Giderme

1. "Failed to fetch" hatası alıyorsanız:
   - Backend'in çalıştığından emin olun
   - API endpoint'lerinin doğru olduğunu kontrol edin
   - CORS ayarlarını kontrol edin

2. Firebird bağlantı hatası alıyorsanız:
   - Firebird servislerinin çalıştığını kontrol edin
   - Veritabanı yolunun doğru olduğunu kontrol edin
   - Kullanıcı adı ve şifrenin doğru olduğunu kontrol edin 