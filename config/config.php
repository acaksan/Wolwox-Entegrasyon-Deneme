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

// Firebird bağlantısı fonksiyonu
if (!function_exists('getFirebirdConnection')) {
    function getFirebirdConnection() {
        static $db = null;
        static $transaction = null;
        
        if ($db === null) {
            try {
                if (!function_exists('ibase_connect')) {
                    throw new Exception('Wolvox bağlantı hatası: Firebird eklentisi yüklü değil. Lütfen php_interbase.dll dosyasını PHP kurulumunuza ekleyin.');
                }

                // Firebird bağlantı bilgileri
                $host = FB_HOST;
                $port = FB_PORT;
                $database = str_replace('\\', '/', FB_DATABASE);
                $username = FB_USERNAME;
                $password = FB_PASSWORD;
                $charset = FB_CHARSET;

                // Bağlantı dizesi oluştur
                $connection_string = $host . '/' . $port . ':' . $database;

                // Firebird'e bağlan
                $db = ibase_connect(
                    $connection_string,
                    $username,
                    $password,
                    $charset
                );

                if (!$db) {
                    throw new Exception('Wolvox bağlantı hatası: ' . ibase_errmsg());
                }

                // Transaction başlat
                $transaction = ibase_trans($db);
                
                if (!$transaction) {
                    throw new Exception('Wolvox transaction hatası: ' . ibase_errmsg());
                }

            } catch (Exception $e) {
                error_log("Veritabanı bağlantı hatası: " . $e->getMessage());
                throw new Exception("Veritabanına bağlanılamadı: " . $e->getMessage());
            }
        }
        
        return [$db, $transaction];
    }
}