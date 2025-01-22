const express = require('express');
const router = express.Router();
const firebirdController = require('../controllers/firebirdController');

// Bağlantı ayarlarını kaydet
router.post('/connection/save', async (req, res) => {
    try {
        const result = await firebirdController.saveConnectionSettings(req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Bağlantıyı test et
router.post('/connection/test', async (req, res) => {
    try {
        const result = await firebirdController.testConnection();
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Ürünleri getir
router.get('/products', async (req, res) => {
    try {
        const result = await firebirdController.getProducts();
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
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

// Ürün stok miktarını getir
router.get('/products/:stokKodu/stock', async (req, res) => {
    try {
        const result = await firebirdController.getProductStock(req.params.stokKodu);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
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

module.exports = router; 