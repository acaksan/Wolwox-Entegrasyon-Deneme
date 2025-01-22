require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const firebirdRoutes = require('./routes/firebirdRoutes');
const wooCommerceRoutes = require('./routes/wooCommerceRoutes');
const productRoutes = require('./routes/productRoutes');

const app = express();
const port = process.env.PORT || 3002;

// Güvenlik middleware'leri
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 dakika
    max: 100 // IP başına maksimum istek sayısı
});
app.use('/api/', limiter);

// CORS ayarları
app.use(cors());

// JSON middleware
app.use(express.json());

// Content-Type ayarı
app.use((req, res, next) => {
    res.setHeader('Content-Type', 'application/json');
    next();
});

// Static dosyalar için klasör tanımla
app.use(express.static(path.join(__dirname, '../../build')));

// API Routes
app.use('/api/firebird', firebirdRoutes);
app.use('/api/woocommerce', wooCommerceRoutes);
app.use('/api/wolvox/products', productRoutes);

// Tüm diğer GET isteklerini React uygulamasına yönlendir
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../../build', 'index.html'));
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        message: 'Sayfa bulunamadı'
    });
});

// Global hata yakalama middleware'i
app.use((err, req, res, next) => {
    console.error('Sunucu hatası:', err);

    // Özel hata mesajları
    const errorMessages = {
        'ECONNREFUSED': 'Veritabanı bağlantısı başarısız',
        'ETIMEDOUT': 'Bağlantı zaman aşımına uğradı',
        'ENOTFOUND': 'Sunucu bulunamadı'
    };

    const statusCode = err.statusCode || 500;
    const errorMessage = errorMessages[err.code] || err.message || 'Sunucu hatası';

    res.status(statusCode).json({
        success: false,
        message: errorMessage,
        error: process.env.NODE_ENV === 'development' ? err.stack : undefined
    });
});

// Sunucuyu başlat
const server = app.listen(port, '0.0.0.0', () => {
    console.log(`Sunucu http://localhost:${port} adresinde çalışıyor`);
    console.log('Ortam:', process.env.NODE_ENV || 'development');
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM sinyali alındı. Sunucu kapatılıyor...');
    server.close(() => {
        console.log('Sunucu kapatıldı');
        process.exit(0);
    });
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('İşlenmeyen Promise reddi:', reason);
});

process.on('uncaughtException', (error) => {
    console.error('İşlenmeyen hata:', error);
    process.exit(1);
}); 