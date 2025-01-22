export const menuStructure = {
    items: [
        {
            id: 'dashboard',
            title: 'DASHBOARD',
            icon: 'fas fa-home',
            active: true,
            items: [
                {
                    id: 'overview',
                    name: 'Genel Bakış',
                    path: '/dashboard',
                    icon: 'fas fa-chart-line',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'sales-stats',
                    name: 'Satış İstatistikleri',
                    path: '/dashboard/sales',
                    icon: 'fas fa-chart-bar',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'stock-status',
                    name: 'Stok Durumu',
                    path: '/dashboard/stock',
                    icon: 'fas fa-boxes',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'critical-alerts',
                    name: 'Kritik Seviye Uyarıları',
                    path: '/dashboard/alerts',
                    icon: 'fas fa-exclamation-triangle',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'products',
            title: 'ÜRÜN YÖNETİMİ',
            icon: 'fas fa-box',
            active: true,
            items: [
                {
                    id: 'product-list',
                    name: 'Ürün Listesi',
                    path: '/products',
                    icon: 'fas fa-list',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'add-product',
                    name: 'Yeni Ürün Ekle',
                    path: '/products/add',
                    icon: 'fas fa-plus',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'bulk-operations',
                    name: 'Toplu Ürün İşlemleri',
                    path: '/products/bulk',
                    icon: 'fas fa-tasks',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'categories',
                    name: 'Kategoriler',
                    path: '/products/categories',
                    icon: 'fas fa-tags',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'brands',
                    name: 'Markalar',
                    path: '/products/brands',
                    icon: 'fas fa-copyright',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'tire-specs',
                    name: 'Lastik Özellikleri',
                    path: '/products/specs',
                    icon: 'fas fa-cog',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'stock',
            title: 'STOK YÖNETİMİ',
            icon: 'fas fa-warehouse',
            active: true,
            items: [
                {
                    id: 'stock-status',
                    name: 'Stok Durumu',
                    path: '/stock',
                    icon: 'fas fa-boxes',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'stock-movements',
                    name: 'Stok Hareketleri',
                    path: '/stock/movements',
                    icon: 'fas fa-exchange-alt',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'warehouse-management',
                    name: 'Depo Yönetimi',
                    path: '/stock/warehouses',
                    icon: 'fas fa-building',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'orders',
            title: 'SİPARİŞ YÖNETİMİ',
            icon: 'fas fa-shopping-cart',
            active: true,
            items: [
                {
                    id: 'all-orders',
                    name: 'Tüm Siparişler',
                    path: '/orders',
                    icon: 'fas fa-list',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'pending-orders',
                    name: 'Bekleyen Siparişler',
                    path: '/orders/pending',
                    icon: 'fas fa-clock',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'shipping',
                    name: 'Kargo Takibi',
                    path: '/orders/shipping',
                    icon: 'fas fa-truck',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'accounts',
            title: 'CARİ HESAP YÖNETİMİ',
            icon: 'fas fa-users',
            active: true,
            items: [
                {
                    id: 'customers',
                    name: 'Müşteriler',
                    path: '/accounts/customers',
                    icon: 'fas fa-user',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'suppliers',
                    name: 'Tedarikçiler',
                    path: '/accounts/suppliers',
                    icon: 'fas fa-truck',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'dealers',
                    name: 'Bayiler',
                    path: '/accounts/dealers',
                    icon: 'fas fa-store',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'ecommerce',
            title: 'E-TİCARET',
            icon: 'fas fa-globe',
            active: true,
            items: [
                {
                    id: 'woocommerce-sync',
                    name: 'WooCommerce Senkronizasyon',
                    path: '/ecommerce/sync',
                    icon: 'fas fa-sync',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'marketplace',
                    name: 'Pazaryeri Entegrasyonları',
                    path: '/ecommerce/marketplace',
                    icon: 'fas fa-store',
                    active: true,
                    status: 'planned'
                }
            ]
        },
        {
            id: 'reports',
            title: 'RAPORLAR',
            icon: 'fas fa-chart-bar',
            active: true,
            items: [
                {
                    id: 'sales-reports',
                    name: 'Satış Raporları',
                    path: '/reports/sales',
                    icon: 'fas fa-chart-line',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'stock-reports',
                    name: 'Stok Raporları',
                    path: '/reports/stock',
                    icon: 'fas fa-boxes',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'financial-reports',
                    name: 'Finansal Raporlar',
                    path: '/reports/financial',
                    icon: 'fas fa-file-invoice-dollar',
                    active: true,
                    status: 'development'
                }
            ]
        },
        {
            id: 'settings',
            title: 'AYARLAR',
            icon: 'fas fa-cog',
            active: true,
            items: [
                {
                    id: 'menu-management',
                    name: 'Menü Yönetimi',
                    path: '/settings/menu',
                    icon: 'fas fa-bars',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'wolvox-settings',
                    name: 'Wolvox Bağlantısı',
                    path: '/settings/wolvox',
                    icon: 'fas fa-database',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'woocommerce-settings',
                    name: 'WooCommerce Ayarları',
                    path: '/settings/woocommerce',
                    icon: 'fas fa-shopping-cart',
                    active: true,
                    status: 'development'
                },
                {
                    id: 'user-management',
                    name: 'Kullanıcı Yönetimi',
                    path: '/settings/users',
                    icon: 'fas fa-users-cog',
                    active: true,
                    status: 'development'
                }
            ]
        }
    ]
} 