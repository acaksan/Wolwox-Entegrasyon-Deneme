<?php
// Database configuration
define('FB_HOST', 'localhost');
define('FB_DATABASE', 'C:\\WolvoxERP\\DATA\\WOLVOX.FDB');
define('FB_USERNAME', 'SYSDBA');
define('FB_PASSWORD', 'masterkey');
define('FB_CHARSET', 'UTF8');
define('FB_CLIENT_LIB', 'C:\\Program Files (x86)\\Firebird\\Firebird_2_5\\fbclient.dll');

// WooCommerce configuration
define('WC_URL', 'your-website.com');
define('WC_CONSUMER_KEY', 'your-consumer-key');
define('WC_CONSUMER_SECRET', 'your-consumer-secret');

// Application configuration
define('APP_NAME', 'Wolvox-WooCommerce Entegrasyon');
define('APP_URL', 'http://localhost/wolvox-woo');
define('DEBUG_MODE', true);

// Menu configuration
$GLOBALS['menu_config'] = [
    'dashboard' => [
        'title' => 'Dashboard',
        'icon' => 'fas fa-tachometer-alt',
        'permission' => 'view_dashboard'
    ],
    'orders' => [
        'title' => 'Siparişler',
        'icon' => 'fas fa-shopping-cart',
        'permission' => 'view_orders',
        'submenu' => [
            'all_orders' => ['title' => 'Tüm Siparişler'],
            'pending_orders' => ['title' => 'Bekleyen Siparişler'],
            'completed_orders' => ['title' => 'Tamamlanan Siparişler']
        ]
    ],
    // Diğer menü öğeleri buraya eklenecek
];

// Error reporting
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}
