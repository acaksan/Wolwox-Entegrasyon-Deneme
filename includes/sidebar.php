<?php
$current_page = isset($_GET['page']) ? $_GET['page'] : 'dashboard';
?>

<nav id="sidebar" class="active">
    <div class="sidebar-header">
        <h3><?php echo APP_NAME; ?></h3>
        <div class="sidebar-toggle">
            <button type="button" id="sidebarCollapse" class="btn">
                <i class="fas fa-bars"></i>
            </button>
        </div>
    </div>

    <ul class="list-unstyled components">
        <?php foreach ($GLOBALS['menu_config'] as $key => $menu_item): ?>
            <?php if (isset($menu_item['permission']) && checkPermission($menu_item['permission'])): ?>
                <li class="<?php echo ($current_page == $key) ? 'active' : ''; ?>">
                    <?php if (isset($menu_item['submenu'])): ?>
                        <a href="#<?php echo $key; ?>Submenu" data-bs-toggle="collapse" 
                           class="dropdown-toggle <?php echo ($current_page == $key) ? '' : 'collapsed'; ?>">
                            <i class="<?php echo $menu_item['icon']; ?>"></i>
                            <span><?php echo $menu_item['title']; ?></span>
                        </a>
                        <ul class="collapse list-unstyled <?php echo ($current_page == $key) ? 'show' : ''; ?>" 
                            id="<?php echo $key; ?>Submenu">
                            <?php foreach ($menu_item['submenu'] as $sub_key => $sub_item): ?>
                                <li class="<?php echo ($current_page == $sub_key) ? 'active' : ''; ?>">
                                    <a href="?page=<?php echo $sub_key; ?>">
                                        <?php echo $sub_item['title']; ?>
                                    </a>
                                </li>
                            <?php endforeach; ?>
                        </ul>
                    <?php else: ?>
                        <a href="?page=<?php echo $key; ?>">
                            <i class="<?php echo $menu_item['icon']; ?>"></i>
                            <span><?php echo $menu_item['title']; ?></span>
                        </a>
                    <?php endif; ?>
                </li>
            <?php endif; ?>
        <?php endforeach; ?>
    </ul>

    <div class="sidebar-footer">
        <div class="version">Version: 1.0.0</div>
    </div>
</nav>

<script>
$(document).ready(function() {
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
    });
});
</script>
