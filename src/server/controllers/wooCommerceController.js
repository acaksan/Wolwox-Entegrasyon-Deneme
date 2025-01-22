const WooCommerceAPI = require('@woocommerce/woocommerce-rest-api').default;
const firebirdController = require('./firebirdController');
require('dotenv').config();

let wooCommerce = null;

// WooCommerce API yapılandırması
const initializeWooCommerce = (settings) => {
    try {
        const config = {
            url: settings?.url || process.env.WOOCOMMERCE_URL,
            consumerKey: settings?.key || process.env.WOOCOMMERCE_KEY,
            consumerSecret: settings?.secret || process.env.WOOCOMMERCE_SECRET,
            version: 'wc/v3',
            queryStringAuth: true,
            timeout: 10000 // 10 saniye timeout
        };

        // Gerekli alanları kontrol et
        if (!config.url || !config.consumerKey || !config.consumerSecret) {
            throw new Error('WooCommerce yapılandırma bilgileri eksik');
        }

        return new WooCommerceAPI(config);
    } catch (error) {
        console.error('WooCommerce başlatma hatası:', error);
        throw error;
    }
};

// Bağlantı durumunu kontrol et
const checkConnection = async () => {
    try {
        if (!wooCommerce) {
            wooCommerce = initializeWooCommerce();
        }
        const response = await wooCommerce.get('system_status');
        return { success: true, status: response.status };
    } catch (error) {
        console.error('WooCommerce bağlantı kontrolü hatası:', error);
        return { success: false, error: error.message };
    }
};

// Fiyat güncelleme fonksiyonu
async function updateProductPrices() {
    try {
        if (!wooCommerce) {
            throw new Error('WooCommerce bağlantısı başlatılmamış');
        }

        // Firebird'den fiyatları al
        const firebirdPrices = await firebirdController.getProductPrices();
        if (!firebirdPrices.success) {
            throw new Error('Firebird\'den fiyatlar alınamadı');
        }

        const updateResults = [];
        
        // Her ürün için WooCommerce'de güncelleme yap
        for (const product of firebirdPrices.data) {
            try {
                // Önce ürünü SKU'ya göre bul
                const searchResponse = await wooCommerce.get('products', {
                    sku: product.barkod
                });

                if (searchResponse.data && searchResponse.data.length > 0) {
                    const wooProduct = searchResponse.data[0];
                    
                    // Fiyatı güncelle
                    const updateResponse = await wooCommerce.put(`products/${wooProduct.id}`, {
                        regular_price: product.satisFiyati.toString(),
                        stock_quantity: null // Stok miktarını ayrı bir fonksiyonda güncelleyeceğiz
                    });

                    updateResults.push({
                        stokKodu: product.stokKodu,
                        barkod: product.barkod,
                        success: true,
                        message: 'Fiyat güncellendi',
                        oldPrice: wooProduct.regular_price,
                        newPrice: product.satisFiyati
                    });
                } else {
                    updateResults.push({
                        stokKodu: product.stokKodu,
                        barkod: product.barkod,
                        success: false,
                        message: 'Ürün WooCommerce\'de bulunamadı'
                    });
                }
            } catch (error) {
                updateResults.push({
                    stokKodu: product.stokKodu,
                    barkod: product.barkod,
                    success: false,
                    message: `Güncelleme hatası: ${error.message}`
                });
            }
        }

        return {
            success: true,
            message: 'Fiyat güncelleme işlemi tamamlandı',
            data: updateResults
        };

    } catch (error) {
        console.error('Fiyat güncelleme hatası:', error);
        return {
            success: false,
            message: 'Fiyat güncelleme işlemi başarısız',
            error: error.message
        };
    }
}

// Bağlantı ayarlarını kaydet ve test et
const saveSettings = async (req, res) => {
    try {
        const { url, key, secret } = req.body;
        
        // Gerekli alanları kontrol et
        if (!url || !key || !secret) {
            return res.status(400).json({
                success: false,
                message: 'Tüm alanlar zorunludur'
            });
        }

        // Test bağlantısı
        wooCommerce = initializeWooCommerce({ url, key, secret });
        const testResult = await checkConnection();
        
        if (!testResult.success) {
            return res.status(400).json({
                success: false,
                message: 'Bağlantı testi başarısız',
                error: testResult.error
            });
        }

        // Ayarları kaydet
        process.env.WOOCOMMERCE_URL = url;
        process.env.WOOCOMMERCE_KEY = key;
        process.env.WOOCOMMERCE_SECRET = secret;

        res.json({
            success: true,
            message: 'WooCommerce ayarları başarıyla kaydedildi'
        });
    } catch (error) {
        console.error('WooCommerce ayarları kaydedilirken hata:', error);
        res.status(500).json({
            success: false,
            message: 'WooCommerce ayarları kaydedilemedi',
            error: error.message
        });
    }
};

// Bağlantıyı test et
const testConnection = async (req, res) => {
    try {
        const result = await checkConnection();
        if (!result.success) {
            return res.status(500).json({
                success: false,
                message: 'WooCommerce bağlantısı başarısız',
                error: result.error
            });
        }

        res.json({
            success: true,
            message: 'WooCommerce bağlantısı başarılı',
            status: result.status
        });
    } catch (error) {
        console.error('WooCommerce bağlantı testi hatası:', error);
        res.status(500).json({
            success: false,
            message: 'WooCommerce bağlantı testi başarısız',
            error: error.message
        });
    }
};

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
    syncOrders,
    updateProductPrices,
    checkConnection
}; 