<?php
// Menü yapısı
function getMenu() {
    return [
        [
            'title' => 'Dashboard',
            'icon' => 'fas fa-tachometer-alt',
            'page' => 'dashboard'
        ],
        [
            'title' => 'Siparişler',
            'icon' => 'fas fa-shopping-cart',
            'page' => 'orders'
        ],
        [
            'title' => 'Müşteriler',
            'icon' => 'fas fa-users',
            'page' => 'customers'
        ],
        [
            'title' => 'Ödemeler',
            'icon' => 'fas fa-credit-card',
            'page' => 'payments'
        ],
        [
            'title' => 'Ürünler',
            'icon' => 'fas fa-box',
            'page' => 'products',
            'submenu' => [
                [
                    'title' => 'Ürün Listesi',
                    'page' => 'products'
                ],
                [
                    'title' => 'Kategori Eşleştirme',
                    'page' => 'products',
                    'params' => ['view' => 'categories']
                ],
                [
                    'title' => 'Toplu İşlemler',
                    'page' => 'products',
                    'params' => ['view' => 'bulk']
                ]
            ]
        ],
        [
            'title' => 'Senkronizasyon',
            'icon' => 'fas fa-sync',
            'page' => 'sync',
            'submenu' => [
                [
                    'title' => 'Durum',
                    'page' => 'sync'
                ],
                [
                    'title' => 'Geçmiş',
                    'page' => 'sync',
                    'params' => ['view' => 'history']
                ],
                [
                    'title' => 'Hata Logları',
                    'page' => 'sync',
                    'params' => ['view' => 'logs']
                ]
            ]
        ],
        [
            'title' => 'Raporlar',
            'icon' => 'fas fa-chart-bar',
            'page' => 'reports',
            'submenu' => [
                [
                    'title' => 'Satış Raporları',
                    'page' => 'reports',
                    'params' => ['type' => 'sales']
                ],
                [
                    'title' => 'Stok Raporları',
                    'page' => 'reports',
                    'params' => ['type' => 'stock']
                ],
                [
                    'title' => 'Müşteri Raporları',
                    'page' => 'reports',
                    'params' => ['type' => 'customers']
                ]
            ]
        ],
        [
            'title' => 'Ayarlar',
            'icon' => 'fas fa-cog',
            'page' => 'settings',
            'submenu' => [
                [
                    'title' => 'Genel Ayarlar',
                    'page' => 'settings'
                ],
                [
                    'title' => 'Stok Ayarları',
                    'page' => 'settings',
                    'params' => ['tab' => 'stock']
                ],
                [
                    'title' => 'Sipariş Ayarları',
                    'page' => 'settings',
                    'params' => ['tab' => 'orders']
                ],
                [
                    'title' => 'Cari Ayarları',
                    'page' => 'settings',
                    'params' => ['tab' => 'customers']
                ]
            ]
        ],
        [
            'title' => 'Yardım',
            'icon' => 'fas fa-question-circle',
            'page' => 'help'
        ]
    ];
}

// URL oluşturma fonksiyonu
function buildUrl($page, $params = []) {
    $query = empty($params) ? '' : '&' . http_build_query($params);
    return "?page={$page}{$query}";
}

// Aktif menü kontrolü
function isActiveMenu($page) {
    $current_page = $_GET['page'] ?? 'dashboard';
    return $page === $current_page ? 'active' : '';
}

// Alt menü aktif kontrolü
function isActiveSubmenu($page, $params = []) {
    if (!isActiveMenu($page)) {
        return '';
    }
    
    foreach ($params as $key => $value) {
        if (!isset($_GET[$key]) || $_GET[$key] !== $value) {
            return '';
        }
    }
    
    return 'active';
}

// Mesaj gösterme fonksiyonları
function displayMessage($message, $type = 'info') {
    $_SESSION['message'] = [
        'text' => $message,
        'type' => $type
    ];
}

function showMessage() {
    if (isset($_SESSION['message'])) {
        $message = $_SESSION['message'];
        echo '<div class="alert alert-' . $message['type'] . ' alert-dismissible fade show" role="alert">';
        echo $message['text'];
        echo '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
        echo '</div>';
        unset($_SESSION['message']);
    }
}
?>
