# Wolvox-WooCommerce Entegrasyon

Wolvox ERP ve WooCommerce arasında entegrasyon sağlayan PHP tabanlı web uygulaması.

## Özellikler

- Modern ve responsive arayüz
- Modüler yapı
- Firebird veritabanı entegrasyonu
- WooCommerce API entegrasyonu
- Ürün, stok ve sipariş senkronizasyonu
- Detaylı raporlama sistemi

## Gereksinimler

- PHP 7.4 veya üzeri
- Firebird 2.5 32-bit Client
- PDO Firebird eklentisi
- Composer
- Web sunucusu (Apache/Nginx)

## Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/acaksan/Wolwox-Entegrasyon-Deneme.git
```

2. Composer bağımlılıklarını yükleyin:
```bash
composer install
```

3. config.php dosyasını düzenleyin:
- Firebird veritabanı bağlantı bilgilerini ayarlayın
- WooCommerce API anahtarlarını ekleyin

4. Web sunucusunu yapılandırın ve uygulamayı çalıştırın

## Geliştirme

```bash
php -S localhost:8000
```

## Lisans

MIT License
