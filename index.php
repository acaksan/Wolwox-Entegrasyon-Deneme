<?php
session_start();
require_once 'includes/functions.php';

// Sayfa yönlendirmesi
$page = isset($_GET['page']) ? $_GET['page'] : 'dashboard';

// Menü öğelerini al
$menuItems = getMenu();

// Sayfa başlığını bul
$pageTitle = 'Dashboard';
foreach ($menuItems as $item) {
    if ($item['page'] === $page) {
        $pageTitle = $item['title'];
        break;
    }
    // Alt menülerde ara
    if (!empty($item['submenu'])) {
        foreach ($item['submenu'] as $subItem) {
            if ($subItem['page'] === $page) {
                $pageTitle = $subItem['title'];
                break 2;
            }
        }
    }
}

// Sayfa dosyasının yolu
$pagePath = "pages/{$page}.php";
?>

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wolvox - WooCommerce Entegrasyon | <?php echo $pageTitle; ?></title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="assets/css/style.css" rel="stylesheet">
</head>
<body>
    <div class="wrapper">
        <!-- Sidebar -->
        <?php include 'includes/sidebar.php'; ?>
        
        <!-- Ana içerik -->
        <div class="content">
            <!-- Header -->
            <?php include 'includes/header.php'; ?>
            
            <!-- Sayfa içeriği -->
            <div class="container-fluid py-4">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1 class="h3"><?php echo $pageTitle; ?></h1>
                </div>
                
                <?php 
                showMessage();
                
                if (file_exists($pagePath)) {
                    include $pagePath;
                } else {
                    echo '<div class="alert alert-danger">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Sayfa bulunamadı
                          </div>';
                }
                ?>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <!-- Custom JS -->
    <script src="assets/js/script.js"></script>
</body>
</html>
