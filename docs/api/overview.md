# API Dokümantasyonu

## Genel Bakış

Bu API, WooCommerce ve Wolvox sistemleri arasında veri senkronizasyonu sağlar.

## Kimlik Doğrulama

API, Bearer token tabanlı kimlik doğrulama kullanır:

```http
Authorization: Bearer <your_token>
```

## Endpoints

### Ürünler

#### Ürün Listesi

```http
GET /api/v1/products
```

Query Parameters:
- `page`: Sayfa numarası (default: 1)
- `limit`: Sayfa başına ürün sayısı (default: 10)
- `category`: Kategori ID
- `search`: Arama terimi

#### Ürün Detayı

```http
GET /api/v1/products/{id}
```

#### Ürün Güncelleme

```http
PUT /api/v1/products/{id}
```

### Siparişler

#### Sipariş Listesi

```http
GET /api/v1/orders
```

#### Sipariş Detayı

```http
GET /api/v1/orders/{id}
```

### Senkronizasyon

#### Ürün Senkronizasyonu

```http
POST /api/v1/sync/products
```

#### Sipariş Senkronizasyonu

```http
POST /api/v1/sync/orders
```

## Hata Kodları

- `400`: Bad Request - İstek parametreleri hatalı
- `401`: Unauthorized - Kimlik doğrulama başarısız
- `403`: Forbidden - Yetkisiz erişim
- `404`: Not Found - Kaynak bulunamadı
- `429`: Too Many Requests - Rate limit aşıldı
- `500`: Internal Server Error - Sunucu hatası

## Rate Limiting

API, dakikada 100 istek ile sınırlıdır. Limit aşıldığında 429 hatası döner.

## Önbellekleme

Ürün listesi ve detayları 5 dakika önbelleklenir. Önbellek Redis'te tutulur.

## Metrikler

Prometheus metrikleri `/metrics` endpoint'inden alınabilir:
- Request sayısı
- Response süreleri
- Hata oranları
- Cache hit/miss oranları
