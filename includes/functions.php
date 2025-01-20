<?php
// URL oluşturma fonksiyonu
function buildUrl($page, $params = []) {
    $url = '?page=' . urlencode($page);
    foreach ($params as $key => $value) {
        $url .= '&' . urlencode($key) . '=' . urlencode($value);
    }
    return $url;
}

// Aktif menü kontrolü
function isActiveMenu($page) {
    $currentPage = $_GET['page'] ?? 'dashboard';
    return $page === $currentPage;
}

// Alt menü aktif kontrolü
function isActiveSubmenu($page, $params = []) {
    if (!isActiveMenu($page)) {
        return false;
    }
    
    foreach ($params as $key => $value) {
        if (!isset($_GET[$key]) || $_GET[$key] != $value) {
            return false;
        }
    }
    
    return true;
}

/**
 * Menü öğelerini döndürür
 * @return array
 */
function getMenu() {
    return [
        'dashboard' => [
            'title' => 'Dashboard',
            'icon' => 'fas fa-tachometer-alt',
            'page' => 'dashboard',
            'permission' => 'view_dashboard'
        ],
        'products' => [
            'title' => 'Ürünler',
            'icon' => 'fas fa-box',
            'page' => 'products',
            'permission' => 'view_products'
        ],
        'orders' => [
            'title' => 'Siparişler',
            'icon' => 'fas fa-shopping-cart',
            'page' => 'orders',
            'permission' => 'view_orders'
        ],
        'customers' => [
            'title' => 'Müşteriler',
            'icon' => 'fas fa-users',
            'page' => 'customers',
            'permission' => 'view_customers'
        ],
        'sync' => [
            'title' => 'Senkronizasyon',
            'icon' => 'fas fa-sync',
            'page' => 'sync',
            'permission' => 'manage_sync'
        ],
        'settings' => [
            'title' => 'Ayarlar',
            'icon' => 'fas fa-cog',
            'page' => 'settings',
            'permission' => 'manage_settings'
        ]
    ];
}

/**
 * Stok verilerini Firebird'den çeker
 * @return array
 */
function getStockData() {
    try {
        $db = Database::getInstance();
        $query = "SELECT FIRST 100
            STOKKODU,
            STOK_ADI,
            BIRIMI,
            KDV_ORANI,
            WEBDE_GORUNSUN,
            AKTIF,
            SATISFIYATI1
        FROM STOK 
        WHERE AKTIF = 1 
        AND WEBDE_GORUNSUN = 1
        ORDER BY STOKKODU";
        
        $stmt = $db->query($query);
        $products = [];
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $products[] = [
                'stok_kodu' => trim($row['STOKKODU']),
                'stok_adi' => trim($row['STOK_ADI']),
                'birim' => trim($row['BIRIMI']),
                'kdv_orani' => floatval($row['KDV_ORANI']),
                'webde_gorunsun' => (bool)$row['WEBDE_GORUNSUN'],
                'aktif' => (bool)$row['AKTIF'],
                'satis_fiyati' => floatval($row['SATISFIYATI1']),
                'stok_miktari' => 0.00 // Stok miktarını daha sonra ekleyeceğiz
            ];
        }
        return $products;
    } catch(PDOException $e) {
        error_log("Stok verisi çekme hatası: " . $e->getMessage());
        throw $e;
    }
}

/**
 * Fiyatı formatlar
 * @param float $price Fiyat
 * @return string
 */
function formatPrice($price) {
    return number_format($price, 2, ',', '.') . ' ₺';
}

/**
 * Tarihi formatlar
 * @param string $date
 * @return string
 */
function formatDate($date) {
    return date('d.m.Y H:i', strtotime($date));
}

/**
 * Mesaj gösterir
 * @param string $message Mesaj
 * @param string $type Mesaj tipi (success, error, warning, info)
 * @return void
 */
function displayMessage($message, $type = 'info') {
    $_SESSION['message'] = [
        'text' => $message,
        'type' => $type
    ];
}

/**
 * Session'daki mesajı gösterir ve siler
 * @return void
 */
function showMessage() {
    if (isset($_SESSION['message'])) {
        $message = $_SESSION['message'];
        $type = match($message['type']) {
            'success' => 'success',
            'error' => 'danger',
            'warning' => 'warning',
            default => 'info'
        };
        
        echo '<div class="alert alert-' . $type . ' alert-dismissible fade show" role="alert">';
        if ($type === 'success') {
            echo '<i class="fas fa-check-circle me-2"></i>';
        } elseif ($type === 'danger') {
            echo '<i class="fas fa-exclamation-triangle me-2"></i>';
        } elseif ($type === 'warning') {
            echo '<i class="fas fa-exclamation-circle me-2"></i>';
        } else {
            echo '<i class="fas fa-info-circle me-2"></i>';
        }
        echo htmlspecialchars($message['text']);
        echo '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        echo '</div>';
        
        unset($_SESSION['message']);
    }
}

/**
 * Sipariş durumunu badge olarak gösterir
 * @param string $status Sipariş durumu
 * @return string HTML badge
 */
function getOrderStatusBadge($status) {
    $badges = [
        'pending' => ['class' => 'warning', 'text' => 'Bekliyor'],
        'processing' => ['class' => 'info', 'text' => 'İşleniyor'],
        'completed' => ['class' => 'success', 'text' => 'Tamamlandı'],
        'cancelled' => ['class' => 'danger', 'text' => 'İptal Edildi'],
        'refunded' => ['class' => 'secondary', 'text' => 'İade Edildi']
    ];
    
    $badge = $badges[$status] ?? ['class' => 'secondary', 'text' => 'Bilinmiyor'];
    return '<span class="badge bg-' . $badge['class'] . '">' . $badge['text'] . '</span>';
}

/**
 * Oturum kontrolü yapar
 * @return void
 */
function checkSession() {
    if (!isset($_SESSION['user_id'])) {
        header('Location: login.php');
        exit;
    }
}

/**
 * CSRF token oluşturur
 * @return string
 */
function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * CSRF token doğrular
 * @param string $token
 * @return bool
 */
function validateCSRFToken($token) {
    if (!isset($_SESSION['csrf_token']) || $token !== $_SESSION['csrf_token']) {
        return false;
    }
    return true;
}

// Error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once __DIR__ . '/../config/config.php';
