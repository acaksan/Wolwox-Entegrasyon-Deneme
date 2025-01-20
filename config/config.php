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
        'permission' => 'view_dashboard',
        'submenu' => [
            'overview' => [
                'title' => 'Genel Bakış',
                'submenu' => [
                    'daily_sales' => ['title' => 'Günlük Satış Özeti'],
                    'pending_orders' => ['title' => 'Bekleyen Siparişler'],
                    'sync_status' => ['title' => 'Senkronizasyon Durumu'],
                    'recent_activities' => ['title' => 'Son İşlemler/Bildirimler']
                ]
            ]
        ]
    ],
    'orders' => [
        'title' => 'Siparişler',
        'icon' => 'fas fa-shopping-cart',
        'permission' => 'view_orders',
        'submenu' => [
            'order_management' => [
                'title' => 'Sipariş Yönetimi',
                'submenu' => [
                    'all_orders' => ['title' => 'Tüm Siparişler'],
                    'new_orders' => ['title' => 'Yeni Siparişler'],
                    'pending_approval' => ['title' => 'Onay Bekleyenler'],
                    'preparing' => ['title' => 'Hazırlananlar'],
                    'shipped' => ['title' => 'Kargoya Verilenler'],
                    'completed' => ['title' => 'Tamamlananlar']
                ]
            ],
            'bulk_operations' => [
                'title' => 'Toplu Sipariş İşlemleri',
                'submenu' => [
                    'bulk_status_update' => ['title' => 'Toplu Durum Güncelleme'],
                    'bulk_invoice' => ['title' => 'Toplu Fatura Oluşturma']
                ]
            ],
            'order_reports' => ['title' => 'Sipariş Raporları']
        ]
    ],
    'customers' => [
        'title' => 'Cari Hesaplar',
        'icon' => 'fas fa-users',
        'permission' => 'view_customers',
        'submenu' => [
            'customer_management' => [
                'title' => 'Müşteri Yönetimi',
                'submenu' => [
                    'all_customers' => ['title' => 'Tüm Müşteriler'],
                    'woo_customers' => ['title' => 'WooCommerce Müşterileri'],
                    'wolvox_customers' => ['title' => 'Wolvox Müşterileri'],
                    'customer_matching' => ['title' => 'Müşteri Eşleştirme']
                ]
            ],
            'customer_transactions' => [
                'title' => 'Cari Hareketler',
                'submenu' => [
                    'balance' => ['title' => 'Borç/Alacak Durumu'],
                    'collection' => ['title' => 'Tahsilat Takibi'],
                    'due_dates' => ['title' => 'Vade Takibi']
                ]
            ],
            'customer_groups' => [
                'title' => 'Müşteri Grupları',
                'submenu' => [
                    'group_definitions' => ['title' => 'Grup Tanımları'],
                    'special_prices' => ['title' => 'Özel Fiyat Listeleri']
                ]
            ],
            'customer_reports' => ['title' => 'Cari Raporlar']
        ]
    ],
    'payments' => [
        'title' => 'Ödeme İşlemleri',
        'icon' => 'fas fa-credit-card',
        'permission' => 'view_payments',
        'submenu' => [
            'payment_tracking' => [
                'title' => 'Ödeme Takibi',
                'submenu' => [
                    'pending_payments' => ['title' => 'Bekleyen Ödemeler'],
                    'completed_payments' => ['title' => 'Tamamlanan Ödemeler'],
                    'refunds' => ['title' => 'İade İşlemleri']
                ]
            ],
            'payment_methods' => [
                'title' => 'Ödeme Yöntemleri',
                'submenu' => [
                    'online_payments' => ['title' => 'Online Ödemeler'],
                    'bank_transfer' => ['title' => 'Havale/EFT'],
                    'cash_on_delivery' => ['title' => 'Kapıda Ödeme']
                ]
            ],
            'invoice_operations' => [
                'title' => 'Fatura İşlemleri',
                'submenu' => [
                    'create_invoice' => ['title' => 'Fatura Oluşturma'],
                    'e_invoice' => ['title' => 'E-Fatura/E-Arşiv'],
                    'invoice_tracking' => ['title' => 'Fatura Takibi']
                ]
            ],
            'payment_reports' => ['title' => 'Ödeme Raporları']
        ]
    ],
    'products' => [
        'title' => 'Ürün Yönetimi',
        'icon' => 'fas fa-box',
        'permission' => 'view_products',
        'submenu' => [
            'product_list' => ['title' => 'Ürün Listesi'],
            'category_management' => ['title' => 'Kategori Yönetimi'],
            'stock_management' => ['title' => 'Stok Yönetimi'],
            'price_management' => ['title' => 'Fiyat Yönetimi']
        ]
    ],
    'sync' => [
        'title' => 'Senkronizasyon',
        'icon' => 'fas fa-sync',
        'permission' => 'view_sync',
        'submenu' => [
            'data_sync' => [
                'title' => 'Veri Senkronizasyonu',
                'submenu' => [
                    'product_sync' => ['title' => 'Ürün Senkronizasyonu'],
                    'customer_sync' => ['title' => 'Müşteri Senkronizasyonu'],
                    'order_sync' => ['title' => 'Sipariş Senkronizasyonu'],
                    'payment_sync' => ['title' => 'Ödeme Senkronizasyonu']
                ]
            ],
            'scheduled_tasks' => ['title' => 'Zamanlanmış Görevler'],
            'sync_history' => ['title' => 'Senkronizasyon Geçmişi']
        ]
    ],
    'reports' => [
        'title' => 'Raporlar',
        'icon' => 'fas fa-chart-bar',
        'permission' => 'view_reports',
        'submenu' => [
            'sales_reports' => [
                'title' => 'Satış Raporları',
                'submenu' => [
                    'daily_monthly_sales' => ['title' => 'Günlük/Aylık Satışlar'],
                    'product_based_sales' => ['title' => 'Ürün Bazlı Satışlar'],
                    'customer_based_sales' => ['title' => 'Müşteri Bazlı Satışlar']
                ]
            ],
            'financial_reports' => [
                'title' => 'Finansal Raporlar',
                'submenu' => [
                    'collection_report' => ['title' => 'Tahsilat Raporu'],
                    'due_analysis' => ['title' => 'Vade Analizi'],
                    'profit_loss' => ['title' => 'Kâr/Zarar Analizi']
                ]
            ],
            'stock_reports' => ['title' => 'Stok Raporları'],
            'custom_reports' => ['title' => 'Özel Raporlar']
        ]
    ],
    'settings' => [
        'title' => 'Ayarlar',
        'icon' => 'fas fa-cog',
        'permission' => 'view_settings',
        'submenu' => [
            'general_settings' => ['title' => 'Genel Ayarlar'],
            'integration_settings' => [
                'title' => 'Entegrasyon Ayarları',
                'submenu' => [
                    'wolvox_connection' => ['title' => 'Wolvox Bağlantısı'],
                    'woo_connection' => ['title' => 'WooCommerce Bağlantısı'],
                    'payment_system' => ['title' => 'Ödeme Sistemi Ayarları']
                ]
            ],
            'user_management' => ['title' => 'Kullanıcı Yönetimi'],
            'document_settings' => ['title' => 'Belge/Fatura Ayarları'],
            'notification_settings' => ['title' => 'Bildirim Ayarları']
        ]
    ],
    'support' => [
        'title' => 'Yardım & Destek',
        'icon' => 'fas fa-question-circle',
        'permission' => 'view_support'
    ]
];

// Error reporting
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}
