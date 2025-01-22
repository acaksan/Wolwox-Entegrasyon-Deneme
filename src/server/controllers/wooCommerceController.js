const WooCommerceRestApi = require('@woocommerce/woocommerce-rest-api').default;

let wooCommerce = null;

// WooCommerce API yapılandırması
function initializeWooCommerce(settings) {
    wooCommerce = new WooCommerceRestApi({
        url: settings.siteUrl,
        consumerKey: settings.consumerKey,
        consumerSecret: settings.consumerSecret,
        version: settings.apiVersion || 'wc/v3'
    });
    return wooCommerce;
}

// Bağlantı ayarlarını kaydet ve test et
async function saveSettings(settings) {
    try {
        // Ayarları kaydet (örneğin veritabanına veya .env dosyasına)
        process.env.WC_URL = settings.siteUrl;
        process.env.WC_KEY = settings.consumerKey;
        process.env.WC_SECRET = settings.consumerSecret;
        process.env.WC_VERSION = settings.apiVersion;

        // WooCommerce bağlantısını başlat
        initializeWooCommerce(settings);
        
        return { success: true, message: 'WooCommerce ayarları başarıyla kaydedildi.' };
    } catch (error) {
        console.error('WooCommerce ayarları kaydedilirken hata:', error);
        throw new Error('WooCommerce ayarları kaydedilemedi.');
    }
}

// Bağlantıyı test et
async function testConnection() {
    try {
        if (!wooCommerce) {
            throw new Error('WooCommerce bağlantısı yapılandırılmamış.');
        }

        // Basit bir API çağrısı yap
        const response = await wooCommerce.get('system_status');
        return { success: true, message: 'WooCommerce bağlantısı başarılı.' };
    } catch (error) {
        console.error('WooCommerce bağlantı testi hatası:', error);
        throw new Error('WooCommerce bağlantı testi başarısız oldu.');
    }
}

// Ürünleri senkronize et
async function syncProducts(products) {
    try {
        if (!wooCommerce) {
            throw new Error('WooCommerce bağlantısı yapılandırılmamış.');
        }

        const results = [];
        for (const product of products) {
            try {
                // Ürünü WooCommerce'de ara
                const searchResponse = await wooCommerce.get('products', {
                    sku: product.STOK_KODU
                });

                let response;
                if (searchResponse.data.length > 0) {
                    // Ürün varsa güncelle
                    response = await wooCommerce.put(`products/${searchResponse.data[0].id}`, {
                        name: product.STOK_ADI,
                        regular_price: product.SATIS_FIYATI1.toString(),
                        sku: product.STOK_KODU,
                        manage_stock: true,
                        stock_quantity: product.MIKTAR
                    });
                } else {
                    // Ürün yoksa yeni ekle
                    response = await wooCommerce.post('products', {
                        name: product.STOK_ADI,
                        regular_price: product.SATIS_FIYATI1.toString(),
                        sku: product.STOK_KODU,
                        manage_stock: true,
                        stock_quantity: product.MIKTAR
                    });
                }
                results.push({
                    stok_kodu: product.STOK_KODU,
                    success: true,
                    message: 'Ürün başarıyla senkronize edildi.'
                });
            } catch (error) {
                results.push({
                    stok_kodu: product.STOK_KODU,
                    success: false,
                    message: error.message
                });
            }
        }
        return { success: true, data: results };
    } catch (error) {
        console.error('Ürün senkronizasyonu hatası:', error);
        throw new Error('Ürün senkronizasyonu başarısız oldu.');
    }
}

// Stok durumunu senkronize et
async function syncStock(stockData) {
    try {
        if (!wooCommerce) {
            throw new Error('WooCommerce bağlantısı yapılandırılmamış.');
        }

        const results = [];
        for (const stock of stockData) {
            try {
                // Ürünü SKU'ya göre bul
                const searchResponse = await wooCommerce.get('products', {
                    sku: stock.STOK_KODU
                });

                if (searchResponse.data.length > 0) {
                    // Stok miktarını güncelle
                    const response = await wooCommerce.put(`products/${searchResponse.data[0].id}`, {
                        stock_quantity: stock.MIKTAR
                    });
                    results.push({
                        stok_kodu: stock.STOK_KODU,
                        success: true,
                        message: 'Stok durumu güncellendi.'
                    });
                } else {
                    results.push({
                        stok_kodu: stock.STOK_KODU,
                        success: false,
                        message: 'Ürün bulunamadı.'
                    });
                }
            } catch (error) {
                results.push({
                    stok_kodu: stock.STOK_KODU,
                    success: false,
                    message: error.message
                });
            }
        }
        return { success: true, data: results };
    } catch (error) {
        console.error('Stok senkronizasyonu hatası:', error);
        throw new Error('Stok senkronizasyonu başarısız oldu.');
    }
}

// Siparişleri senkronize et
async function syncOrders(startDate, endDate, status) {
    try {
        if (!wooCommerce) {
            throw new Error('WooCommerce bağlantısı yapılandırılmamış.');
        }

        // Siparişleri getir
        const params = {
            after: startDate,
            before: endDate,
            per_page: 100
        };
        if (status) {
            params.status = status;
        }

        const response = await wooCommerce.get('orders', params);
        return { success: true, data: response.data };
    } catch (error) {
        console.error('Sipariş senkronizasyonu hatası:', error);
        throw new Error('Sipariş senkronizasyonu başarısız oldu.');
    }
}

module.exports = {
    initializeWooCommerce,
    saveSettings,
    testConnection,
    syncProducts,
    syncStock,
    syncOrders
}; 