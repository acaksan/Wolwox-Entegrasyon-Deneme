<?php
require_once __DIR__ . '/../includes/functions.php';
?>

<div class="sidebar">
    <div class="sidebar-header">
        <h3>Wolvox Entegrasyon</h3>
        <button class="btn btn-link d-md-none" id="sidebarClose">
            <i class="fas fa-times"></i>
        </button>
    </div>
    
    <ul class="nav flex-column">
        <?php foreach (getMenu() as $menuItem): ?>
            <?php 
            $hasSubmenu = !empty($menuItem['submenu']);
            $menuId = 'menu-' . md5($menuItem['title']);
            $isActive = isActiveMenu($menuItem['page']);
            ?>
            <li class="nav-item">
                <?php if ($hasSubmenu): ?>
                    <a class="nav-link dropdown-toggle <?php echo $isActive ? 'active' : ''; ?>" 
                       href="#" 
                       role="button"
                       onclick="toggleSubmenu('<?php echo $menuId; ?>', event)">
                        <i class="<?php echo $menuItem['icon']; ?> me-2"></i>
                        <span><?php echo $menuItem['title']; ?></span>
                        <i class="fas fa-chevron-down float-end mt-1"></i>
                    </a>
                    <div class="submenu collapse" id="<?php echo $menuId; ?>">
                        <ul class="nav flex-column ms-3">
                            <?php foreach ($menuItem['submenu'] as $submenuItem): ?>
                                <li class="nav-item">
                                    <a class="nav-link <?php echo isActiveSubmenu($submenuItem['page'], $submenuItem['params'] ?? []); ?>" 
                                       href="<?php echo buildUrl($submenuItem['page'], $submenuItem['params'] ?? []); ?>">
                                        <i class="fas fa-circle-dot me-2 small"></i>
                                        <?php echo $submenuItem['title']; ?>
                                    </a>
                                </li>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                <?php else: ?>
                    <a class="nav-link <?php echo $isActive ? 'active' : ''; ?>" 
                       href="<?php echo buildUrl($menuItem['page']); ?>">
                        <i class="<?php echo $menuItem['icon']; ?> me-2"></i>
                        <span><?php echo $menuItem['title']; ?></span>
                    </a>
                <?php endif; ?>
            </li>
        <?php endforeach; ?>
    </ul>
</div>

<style>
.sidebar {
    min-width: 250px;
    max-width: 250px;
    min-height: 100vh;
    background: #f8f9fa;
    padding: 1rem;
    transition: all 0.3s;
}

.sidebar-header {
    padding-bottom: 1rem;
    border-bottom: 1px solid #dee2e6;
}

.sidebar .nav-link {
    color: #333;
    padding: 0.5rem 1rem;
    display: flex;
    align-items: center;
    text-decoration: none;
}

.sidebar .nav-link:hover {
    background: #e9ecef;
    border-radius: 4px;
}

.sidebar .nav-link.active {
    background: #e9ecef;
    border-radius: 4px;
}

.sidebar .submenu {
    padding-left: 1rem;
    overflow: hidden;
    max-height: 0;
    transition: max-height 0.3s ease-out;
}

.sidebar .submenu.show {
    max-height: 500px;
    transition: max-height 0.3s ease-in;
}

.sidebar .submenu .nav-link {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
}

.sidebar .fa-chevron-down {
    transition: transform 0.3s;
}

.sidebar .nav-link[aria-expanded="true"] .fa-chevron-down {
    transform: rotate(180deg);
}

@media (max-width: 768px) {
    .sidebar {
        margin-left: -250px;
    }
    .sidebar.show {
        margin-left: 0;
    }
}
</style>

<script>
function toggleSubmenu(menuId, event) {
    event.preventDefault();
    const submenu = document.getElementById(menuId);
    const allSubmenus = document.querySelectorAll('.submenu');
    
    // Diğer tüm alt menüleri kapat
    allSubmenus.forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove('show');
        }
    });
    
    // Tıklanan menüyü aç/kapat
    submenu.classList.toggle('show');
}

// Sayfa yüklendiğinde aktif menüyü aç
document.addEventListener('DOMContentLoaded', function() {
    const activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        const submenu = activeLink.nextElementSibling;
        if (submenu && submenu.classList.contains('submenu')) {
            submenu.classList.add('show');
        }
    }
    
    // Mobil menü kapatma
    const sidebarClose = document.getElementById('sidebarClose');
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.remove('show');
        });
    }
});
</script>
