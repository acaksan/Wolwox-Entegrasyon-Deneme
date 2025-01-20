<?php 
require_once 'functions.php';
$currentPage = isset($_GET['page']) ? Security::sanitizeInput($_GET['page']) : 'dashboard';
?>

<nav id="sidebar">
    <div class="sidebar-header">
        <h3>Wolvox - WooCommerce</h3>
        <button type="button" id="sidebarCollapse" class="btn">
            <i class="fas fa-bars"></i>
        </button>
    </div>

    <ul class="list-unstyled components">
        <?php 
        $menuItems = getMenu();
        foreach ($menuItems as $key => $item): 
            // İzinleri kontrol et
            if (!isset($_SESSION['permissions']) || !in_array($item['permission'], $_SESSION['permissions'])) {
                continue;
            }
            
            $isActive = $currentPage === $key;
        ?>
            <li class="<?php echo $isActive ? 'active' : ''; ?>">
                <a href="index.php?page=<?php echo urlencode($key); ?>">
                    <i class="<?php echo htmlspecialchars($item['icon']); ?>"></i>
                    <span><?php echo htmlspecialchars($item['title']); ?></span>
                </a>
            </li>
        <?php endforeach; ?>
    </ul>
</nav>

<script>
$(document).ready(function() {
    // Sidebar toggle
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        $('#content').toggleClass('active');
    });

    // Aktif menü öğesine scroll
    if ($('#sidebar li.active').length) {
        $('#sidebar').animate({
            scrollTop: $('#sidebar li.active').offset().top - 100
        }, 200);
    }
});
</script>
