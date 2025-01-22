const express = require('express');
const router = express.Router();
const firebirdController = require('../controllers/firebirdController');

// Mevcut ayarları getir
router.get('/settings', async (req, res) => {
    try {
        // .env dosyasından ayarları oku
        const settings = {
            host: process.env.FIREBIRD_HOST || 'localhost',
            port: process.env.FIREBIRD_PORT || '3050',
            database: process.env.FIREBIRD_DATABASE || '',
            username: process.env.FIREBIRD_USER || 'SYSDBA',
            password: process.env.FIREBIRD_PASSWORD || 'masterkey',
            charset: process.env.FIREBIRD_CHARSET || 'WIN1254'
        };
        
        res.json(settings);
    } catch (error) {
        console.error('Ayarlar getirilirken hata:', error);
        res.status(500).json({
            success: false,
            message: 'Ayarlar getirilemedi'
        });
    }
});

// Bağlantı ayarlarını kaydet
router.post('/settings', async (req, res) => {
    try {
        const result = await firebirdController.saveConnectionSettings(req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Bağlantıyı test et
router.post('/test', async (req, res) => {
    try {
        const result = await firebirdController.testConnection(req.body);
        res.json(result);
    } catch (error) {
        console.error('Test endpoint hatası:', error);
        res.status(500).json({
            success: false,
            message: 'Bağlantı testi başarısız: ' + error.message
        });
    }
});

// Ürünleri getir
router.get('/products', async (req, res) => {
    try {
        const result = await firebirdController.getProducts();
        res.json(result);
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Stok durumunu getir
router.get('/stock/:stokKodu', async (req, res) => {
    try {
        const result = await firebirdController.getProductStock(req.params.stokKodu);
        res.json(result);
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Stok seviyelerini getir
router.get('/stock-levels', async (req, res) => {
    try {
        const result = await firebirdController.getStockLevels();
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Siparişleri getir
router.get('/orders', async (req, res) => {
    try {
        const { startDate, endDate, status } = req.query;
        const result = await firebirdController.getOrders(startDate, endDate, status);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Bağlantıyı test et
router.get('/test', async (req, res) => {
    try {
        const result = await firebirdController.testConnection();
        res.json(result);
    } catch (error) {
        console.error('Test endpoint hatası:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Bağlantı testi başarısız',
            error: error.message 
        });
    }
});

// Stok listesini getir (test için)
router.get('/stoklar', async (req, res) => {
    try {
        const sql = `
            SELECT FIRST 10 
                STOK_KODU, 
                STOK_ADI, 
                SATIS_FIYATI1, 
                MIKTAR 
            FROM STOKLAR 
            WHERE AKTIF = 1
        `;
        const result = await firebirdController.getProducts();
        res.json(result);
    } catch (error) {
        console.error('Stok listesi hatası:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Stok listesi alınamadı',
            error: error.message 
        });
    }
});

// Tüm ürünlerin stok miktarlarını getir
router.get('/stock', async (req, res) => {
    try {
        const result = await firebirdController.getAllProductsStock();
        res.json(result);
    } catch (error) {
        console.error('Stok miktarları getirme hatası:', error);
        res.status(500).json({
            success: false,
            message: 'Stok miktarları getirilemedi',
            error: error.message
        });
    }
});

// Ürün resimlerini getir
router.get('/products/:stokKodu/images', async (req, res) => {
    try {
        const result = await firebirdController.getProductImages(req.params.stokKodu);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Fiyat bilgilerini getir
router.get('/prices', async (req, res) => {
    try {
        const result = await firebirdController.getProductPrices();
        res.json(result);
    } catch (error) {
        console.error('Fiyat bilgileri getirilemedi:', error);
        res.status(500).json({
            success: false,
            message: 'Fiyat bilgileri getirilemedi',
            error: error.message
        });
    }
});

module.exports = router; 