<?php
session_start();
// Gerekli dosyaları dahil et
require_once 'config/config.php';
require_once 'includes/Security.php';
require_once 'includes/Database.php';
require_once 'includes/functions.php';

// Security sınıfını başlat
$security = Security::getInstance();

try {
    // Veritabanı bağlantısını kontrol et
    if (!extension_loaded('pdo_firebird')) {
        throw new Exception('PDO Firebird eklentisi yüklü değil.');
    }
    $db = Database::getInstance();

    // Test amaçlı kullanıcı izinleri
    $_SESSION['permissions'] = [
        'view_dashboard',
        'view_products',
        'manage_products',
        'manage_categories',
        'view_orders',
        'view_customers',
        'manage_sync',
        'manage_settings'
    ];

    // Sayfa yönlendirmesi
    $page = isset($_GET['page']) ? Security::sanitizeInput($_GET['page']) : 'dashboard';
    $pagePath = __DIR__ . "/pages/{$page}.php";
    
    if (!Security::validatePath($pagePath, __DIR__ . '/pages')) {
        $page = 'dashboard';
        $pagePath = __DIR__ . "/pages/dashboard.php";
    }

} catch (Exception $e) {
    error_log($e->getMessage());
    $error = DEBUG_MODE ? $e->getMessage() : 'Bir hata oluştu. Lütfen daha sonra tekrar deneyin.';
}
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wolvox - WooCommerce Entegrasyon</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="assets/css/style.css" rel="stylesheet">
    <link href="assets/css/sidebar.css" rel="stylesheet">
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <div class="wrapper">
        <!-- Sidebar -->
        <?php include 'includes/sidebar.php'; ?>

        <!-- Page Content -->
        <div id="content">
            <?php if (isset($error)): ?>
                <div class="alert alert-danger" role="alert">
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php else: ?>
                <?php 
                if (file_exists($pagePath)) {
                    include $pagePath;
                } else {
                    echo '<div class="alert alert-danger">Sayfa bulunamadı.</div>';
                }
                ?>
            <?php endif; ?>
        </div>
    </div>

    <!-- Custom JS -->
    <script src="assets/js/script.js"></script>
</body>
</html>
