export const menuConfig = {
    items: [
        {
            id: 'dashboard',
            title: 'DASHBOARD',
            icon: 'fas fa-tachometer-alt',
            items: [
                {
                    id: 'overview',
                    name: 'Genel Bakış',
                    path: '/dashboard/overview',
                    icon: 'fas fa-chart-line'
                },
                {
                    id: 'sales-stats',
                    name: 'Satış İstatistikleri',
                    path: '/dashboard/sales',
                    icon: 'fas fa-chart-bar'
                },
                {
                    id: 'stock-status',
                    name: 'Stok Durumu',
                    path: '/dashboard/stock',
                    icon: 'fas fa-boxes'
                },
                {
                    id: 'critical-alerts',
                    name: 'Kritik Seviye Uyarıları',
                    path: '/dashboard/alerts',
                    icon: 'fas fa-exclamation-triangle'
                }
            ]
        },
        {
            id: 'products',
            title: 'ÜRÜN YÖNETİMİ',
            icon: 'fas fa-box',
            items: [
                {
                    id: 'products-main',
                    name: 'Ürünler',
                    icon: 'fas fa-boxes',
                    items: [
                        {
                            id: 'product-list',
                            name: 'Ürün Listesi',
                            path: '/products/list',
                            icon: 'fas fa-list'
                        },
                        {
                            id: 'add-product',
                            name: 'Yeni Ürün Ekle',
                            path: '/products/add',
                            icon: 'fas fa-plus-circle'
                        },
                        {
                            id: 'bulk-operations',
                            name: 'Toplu Ürün İşlemleri',
                            path: '/products/bulk',
                            icon: 'fas fa-tasks'
                        },
                        {
                            id: 'import-export',
                            name: 'Ürün Import/Export',
                            path: '/products/import-export',
                            icon: 'fas fa-exchange-alt'
                        }
                    ]
                },
                {
                    id: 'categories',
                    name: 'Kategoriler',
                    icon: 'fas fa-tags',
                    items: [
                        {
                            id: 'category-tree',
                            name: 'Kategori Ağacı',
                            path: '/products/categories/tree',
                            icon: 'fas fa-sitemap'
                        },
                        {
                            id: 'category-mapping',
                            name: 'Kategori Eşleştirme',
                            path: '/products/categories/mapping',
                            icon: 'fas fa-link'
                        },
                        {
                            id: 'category-templates',
                            name: 'Kategori Şablonları',
                            path: '/products/categories/templates',
                            icon: 'fas fa-copy'
                        }
                    ]
                },
                {
                    id: 'tire-specs',
                    name: 'Lastik Özellikleri',
                    icon: 'fas fa-cog',
                    items: [
                        {
                            id: 'dimensions',
                            name: 'Ebatlar',
                            path: '/products/specs/dimensions',
                            icon: 'fas fa-ruler-combined'
                        },
                        {
                            id: 'seasons',
                            name: 'Mevsim Tipleri',
                            path: '/products/specs/seasons',
                            icon: 'fas fa-sun'
                        },
                        {
                            id: 'speed-codes',
                            name: 'Hız Kodları',
                            path: '/products/specs/speed-codes',
                            icon: 'fas fa-tachometer-alt'
                        },
                        {
                            id: 'load-indexes',
                            name: 'Yük Endeksleri',
                            path: '/products/specs/load-indexes',
                            icon: 'fas fa-weight-hanging'
                        },
                        {
                            id: 'spec-sets',
                            name: 'Özellik Setleri',
                            path: '/products/specs/sets',
                            icon: 'fas fa-layer-group'
                        }
                    ]
                },
                {
                    id: 'brands',
                    name: 'Markalar',
                    icon: 'fas fa-copyright',
                    items: [
                        {
                            id: 'brand-management',
                            name: 'Marka Yönetimi',
                            path: '/products/brands/management',
                            icon: 'fas fa-tasks'
                        },
                        {
                            id: 'brand-categories',
                            name: 'Marka-Kategori İlişkileri',
                            path: '/products/brands/categories',
                            icon: 'fas fa-project-diagram'
                        }
                    ]
                }
            ]
        },
        {
            id: 'stock',
            title: 'STOK YÖNETİMİ',
            icon: 'fas fa-warehouse',
            items: [
                {
                    id: 'stock-status',
                    name: 'Stok Durumu',
                    icon: 'fas fa-boxes',
                    items: [
                        {
                            id: 'general-stock',
                            name: 'Genel Stok Listesi',
                            path: '/stock/list',
                            icon: 'fas fa-list'
                        },
                        {
                            id: 'warehouse-stock',
                            name: 'Depo Bazlı Stoklar',
                            path: '/stock/warehouse',
                            icon: 'fas fa-warehouse'
                        },
                        {
                            id: 'critical-stock',
                            name: 'Kritik Stok Seviyeleri',
                            path: '/stock/critical',
                            icon: 'fas fa-exclamation-triangle'
                        }
                    ]
                },
                {
                    id: 'stock-movements',
                    name: 'Stok Hareketleri',
                    icon: 'fas fa-exchange-alt',
                    items: [
                        {
                            id: 'movement-records',
                            name: 'Giriş/Çıkış Kayıtları',
                            path: '/stock/movements/records',
                            icon: 'fas fa-clipboard-list'
                        },
                        {
                            id: 'transfer-operations',
                            name: 'Transfer İşlemleri',
                            path: '/stock/movements/transfers',
                            icon: 'fas fa-truck'
                        },
                        {
                            id: 'movement-history',
                            name: 'Hareket Geçmişi',
                            path: '/stock/movements/history',
                            icon: 'fas fa-history'
                        }
                    ]
                },
                {
                    id: 'warehouse-management',
                    name: 'Depo Yönetimi',
                    icon: 'fas fa-warehouse',
                    items: [
                        {
                            id: 'warehouse-list',
                            name: 'Depo Listesi',
                            path: '/stock/warehouse/list',
                            icon: 'fas fa-list'
                        },
                        {
                            id: 'warehouse-layout',
                            name: 'Depo Düzeni',
                            path: '/stock/warehouse/layout',
                            icon: 'fas fa-th'
                        },
                        {
                            id: 'shelf-system',
                            name: 'Raf Sistemi',
                            path: '/stock/warehouse/shelves',
                            icon: 'fas fa-layer-group'
                        }
                    ]
                },
                {
                    id: 'inventory-count',
                    name: 'Sayım İşlemleri',
                    icon: 'fas fa-clipboard-check',
                    items: [
                        {
                            id: 'new-count',
                            name: 'Yeni Sayım',
                            path: '/stock/inventory/new',
                            icon: 'fas fa-plus'
                        },
                        {
                            id: 'count-history',
                            name: 'Sayım Geçmişi',
                            path: '/stock/inventory/history',
                            icon: 'fas fa-history'
                        },
                        {
                            id: 'count-reports',
                            name: 'Sayım Raporları',
                            path: '/stock/inventory/reports',
                            icon: 'fas fa-file-alt'
                        }
                    ]
                }
            ]
        }
    ]
} 