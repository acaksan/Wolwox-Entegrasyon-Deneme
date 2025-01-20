<?php

// Yetki kontrolü
function checkPermission($permission) {
    // TODO: Kullanıcı yetki sistemi entegre edildiğinde güncellenecek
    return true;
}

// Firebird bağlantısı
function getFirebirdConnection() {
    static $connection = null;
    
    if ($connection === null) {
        try {
            putenv("FIREBIRD=" . FB_CLIENT_LIB);
            $dsn = "firebird:dbname=" . FB_HOST . ":" . FB_DATABASE . ";charset=" . FB_CHARSET;
            $connection = new PDO($dsn, FB_USERNAME, FB_PASSWORD);
            $connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            error_log("Database connection failed: " . $e->getMessage());
            throw new Exception("Veritabanı bağlantısı kurulamadı.");
        }
    }
    
    return $connection;
}

// Güvenli string
function sanitize($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

// Para formatı
function formatMoney($amount) {
    return number_format($amount, 2, ',', '.');
}

// Tarih formatı
function formatDate($date, $format = 'd.m.Y H:i') {
    return date($format, strtotime($date));
}

// Ajax yanıtı
function jsonResponse($success, $message = '', $data = null) {
    header('Content-Type: application/json');
    echo json_encode([
        'success' => $success,
        'message' => $message,
        'data' => $data
    ]);
    exit;
}

// Menü aktif kontrolü
function isMenuActive($page) {
    $current_page = isset($_GET['page']) ? $_GET['page'] : 'dashboard';
    return $current_page === $page;
}

// Hata mesajı
function showError($message) {
    return '<div class="alert alert-danger" role="alert">' . $message . '</div>';
}

// Başarı mesajı
function showSuccess($message) {
    return '<div class="alert alert-success" role="alert">' . $message . '</div>';
}

// Bilgi mesajı
function showInfo($message) {
    return '<div class="alert alert-info" role="alert">' . $message . '</div>';
}

// Sayfalama
function pagination($total, $per_page, $current_page, $url) {
    $total_pages = ceil($total / $per_page);
    
    if ($total_pages <= 1) return '';
    
    $html = '<nav aria-label="Sayfalama"><ul class="pagination justify-content-center">';
    
    // Önceki sayfa
    if ($current_page > 1) {
        $html .= sprintf(
            '<li class="page-item"><a class="page-link" href="%s">Önceki</a></li>',
            sprintf($url, $current_page - 1)
        );
    }
    
    // Sayfa numaraları
    for ($i = max(1, $current_page - 2); $i <= min($total_pages, $current_page + 2); $i++) {
        $html .= sprintf(
            '<li class="page-item %s"><a class="page-link" href="%s">%d</a></li>',
            $i == $current_page ? 'active' : '',
            sprintf($url, $i),
            $i
        );
    }
    
    // Sonraki sayfa
    if ($current_page < $total_pages) {
        $html .= sprintf(
            '<li class="page-item"><a class="page-link" href="%s">Sonraki</a></li>',
            sprintf($url, $current_page + 1)
        );
    }
    
    $html .= '</ul></nav>';
    
    return $html;
}
