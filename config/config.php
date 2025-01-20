<?php
// Debug modu
define('DEBUG_MODE', true);

// Session ayarları - session başlamadan önce ayarlanmalı
if (session_status() == PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.use_only_cookies', 1);
    ini_set('session.cookie_secure', isset($_SERVER['HTTPS']));
    session_start();
}

// Firebird veritabanı ayarları
define('FB_HOST', 'localhost');  // 127.0.0.1 yerine localhost kullan
define('FB_DATABASE', 'D:\AKINSOFT\Wolvox8\Database_FB\100\2024\WOLVOX.FDB');  // Ters slash düzeltildi
define('FB_USERNAME', 'SYSDBA');
define('FB_PASSWORD', 'masterkey');
define('FB_CHARSET', 'UTF8');  // WIN1254 yerine UTF8 kullan
define('FB_PORT', '3050');  // 3055 yerine varsayılan port 3050'yi kullan

// WooCommerce API ayarları
define('WC_URL', 'https://example.com');
define('WC_CONSUMER_KEY', 'your_consumer_key');
define('WC_CONSUMER_SECRET', 'your_consumer_secret');

// Hata raporlama ayarları
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Timezone ayarı
date_default_timezone_set('Europe/Istanbul');

// PDO Firebird bağlantı fonksiyonu
if (!function_exists('getFirebirdConnection')) {
    function getFirebirdConnection() {
        static $pdo = null;
        
        if ($pdo === null) {
            try {
                if (!extension_loaded('pdo_firebird')) {
                    throw new Exception('Wolvox bağlantı hatası: Firebird eklentisi yüklü değil. Lütfen php_interbase.dll dosyasını PHP kurulumunuza ekleyin.');
                }

                // DSN formatı: firebird:dbname=hostname/port:database
                $dsn = sprintf(
                    'firebird:dbname=%s/%s:%s',  // charset parametresini kaldır
                    FB_HOST,
                    FB_PORT,
                    str_replace('\\', '/', FB_DATABASE)  // Ters slashları düz slasha çevir
                );

                $options = [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::ATTR_EMULATE_PREPARES => false,
                    PDO::ATTR_STRINGIFY_FETCHES => false,
                    PDO::ATTR_CASE => PDO::CASE_NATURAL
                ];

                $pdo = new PDO($dsn, FB_USERNAME, FB_PASSWORD, $options);
                
                // Karakter seti ayarla
                $pdo->exec("SET NAMES '" . FB_CHARSET . "'");
                
            } catch (PDOException $e) {
                error_log("Veritabanı bağlantı hatası: " . $e->getMessage());
                throw new Exception("Veritabanına bağlanılamadı: " . $e->getMessage());
            }
        }
        
        return $pdo;
    }
}
