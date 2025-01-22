const express = require('express');
const router = express.Router();
const wooCommerceController = require('../controllers/wooCommerceController');

// WooCommerce ayarlarını kaydet
router.post('/settings/save', async (req, res) => {
    try {
        const result = await wooCommerceController.saveSettings(req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// WooCommerce bağlantısını test et
router.post('/settings/test', async (req, res) => {
    try {
        const result = await wooCommerceController.testConnection();
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Ürünleri senkronize et
router.post('/products/sync', async (req, res) => {
    try {
        const result = await wooCommerceController.syncProducts(req.body.products);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Stok durumunu senkronize et
router.post('/stock/sync', async (req, res) => {
    try {
        const result = await wooCommerceController.syncStock(req.body.stockData);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Siparişleri senkronize et
router.get('/orders/sync', async (req, res) => {
    try {
        const { startDate, endDate, status } = req.query;
        const result = await wooCommerceController.syncOrders(startDate, endDate, status);
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router; 