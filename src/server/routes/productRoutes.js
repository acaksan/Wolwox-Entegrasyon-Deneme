const express = require('express');
const router = express.Router();
const productController = require('../controllers/productController');

// Ürün karşılaştırma endpoint'i
router.get('/comparison', productController.getProductComparison);

module.exports = router; 