<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo APP_NAME; ?></title>
    
    <!-- CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
    
    <!-- JavaScript -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom Scripts -->
    <script src="assets/js/main.js"></script>
</head>
<body>
    <div id="app-loader" class="d-none">
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Yükleniyor...</span>
        </div>
    </div>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <!-- Mobil menü toggle butonu -->
            <button class="btn btn-link menu-toggle d-md-none">
                <i class="fas fa-bars"></i>
            </button>

            <!-- Başlık -->
            <span class="navbar-brand"><?php echo htmlspecialchars($pageTitle); ?></span>

            <!-- Sağ menü -->
            <div class="ms-auto d-flex align-items-center">
                <!-- Bildirimler -->
                <div class="dropdown me-3">
                    <button class="btn btn-link position-relative" type="button" id="notificationsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-bell"></i>
                        <?php if (isset($_SESSION['notifications']) && count($_SESSION['notifications']) > 0): ?>
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                <?php echo count($_SESSION['notifications']); ?>
                            </span>
                        <?php endif; ?>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="notificationsDropdown">
                        <?php if (isset($_SESSION['notifications']) && count($_SESSION['notifications']) > 0): ?>
                            <?php foreach ($_SESSION['notifications'] as $notification): ?>
                                <li>
                                    <a class="dropdown-item" href="<?php echo htmlspecialchars($notification['link']); ?>">
                                        <i class="<?php echo htmlspecialchars($notification['icon']); ?> me-2"></i>
                                        <?php echo htmlspecialchars($notification['message']); ?>
                                    </a>
                                </li>
                            <?php endforeach; ?>
                        <?php else: ?>
                            <li><span class="dropdown-item">Bildirim bulunmuyor</span></li>
                        <?php endif; ?>
                    </ul>
                </div>

                <!-- Kullanıcı menüsü -->
                <div class="dropdown">
                    <button class="btn btn-link" type="button" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fas fa-user-circle me-1"></i>
                        <span class="d-none d-md-inline">
                            <?php echo htmlspecialchars($_SESSION['user_name'] ?? 'Kullanıcı'); ?>
                        </span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                        <li>
                            <a class="dropdown-item" href="<?php echo buildUrl('profile'); ?>">
                                <i class="fas fa-user me-2"></i>Profil
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="<?php echo buildUrl('settings'); ?>">
                                <i class="fas fa-cog me-2"></i>Ayarlar
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item text-danger" href="<?php echo buildUrl('logout'); ?>">
                                <i class="fas fa-sign-out-alt me-2"></i>Çıkış
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
