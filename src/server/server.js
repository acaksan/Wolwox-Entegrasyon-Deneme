require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const firebirdRoutes = require('./routes/firebirdRoutes');
const wooCommerceRoutes = require('./routes/wooCommerceRoutes');

const app = express();
const port = process.env.PORT || 3001;

// CORS ayarları
app.use(cors({
    origin: ['http://localhost:3000', 'http://localhost:3001'],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static dosyalar için klasör tanımla
app.use(express.static(path.join(__dirname, '../../build')));

// API Routes
app.use('/api/firebird', firebirdRoutes);
app.use('/api/woocommerce', wooCommerceRoutes);

// Tüm diğer GET isteklerini React uygulamasına yönlendir
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../../build', 'index.html'));
});

// Global hata yakalama middleware'i
app.use((err, req, res, next) => {
    console.error('Hata:', err.stack);
    res.status(500).json({
        success: false,
        message: 'Sunucu hatası oluştu',
        error: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// Sunucuyu başlat
app.listen(port, '0.0.0.0', () => {
    console.log(`Sunucu http://localhost:${port} adresinde çalışıyor`);
    console.log('Ortam:', process.env.NODE_ENV || 'development');
}); 