<?php
// Session timeout settings
ini_set('session.gc_maxlifetime', 3600);
session_set_cookie_params(3600);

session_start();
require_once 'config/config.php';
require_once 'includes/functions.php';
require_once 'includes/header.php';
?>

<div class="wrapper">
    <!-- Sidebar -->
    <?php include 'includes/sidebar.php'; ?>

    <!-- Page Content -->
    <div id="content">
        <!-- Top Navbar -->
        <?php include 'includes/navbar.php'; ?>

        <!-- Main Content -->
        <div class="container-fluid">
            <?php
            $page = isset($_GET['page']) ? $_GET['page'] : 'dashboard';
            $file = 'pages/' . $page . '.php';
            
            if (file_exists($file)) {
                include $file;
            } else {
                include 'pages/404.php';
            }
            ?>
        </div>
    </div>
</div>

<?php require_once 'includes/footer.php'; ?>
