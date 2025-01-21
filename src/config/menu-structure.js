export const menuConfig = {
  items: [
    {
      id: 'dashboard',
      title: 'Dashboard',
      icon: 'fas fa-chart-line',
      items: [
        {
          id: 'overview',
          name: 'Genel Bakış',
          path: '/dashboard/overview',
          icon: 'fas fa-home'
        },
        {
          id: 'sales-stats',
          name: 'Satış İstatistikleri',
          path: '/dashboard/sales-stats',
          icon: 'fas fa-chart-bar'
        },
        {
          id: 'stock-status',
          name: 'Stok Durumu',
          path: '/dashboard/stock-status',
          icon: 'fas fa-boxes'
        },
        {
          id: 'critical-alerts',
          name: 'Kritik Seviye Uyarıları',
          path: '/dashboard/critical-alerts',
          icon: 'fas fa-exclamation-triangle'
        }
      ]
    },
    {
      id: 'products',
      title: 'Ürün Yönetimi',
      icon: 'fas fa-box',
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
          icon: 'fas fa-plus'
        },
        {
          id: 'bulk-operations',
          name: 'Toplu İşlemler',
          path: '/products/bulk',
          icon: 'fas fa-layer-group'
        },
        {
          id: 'import-export',
          name: 'İçe/Dışa Aktar',
          path: '/products/import-export',
          icon: 'fas fa-exchange-alt'
        }
      ]
    },
    {
      id: 'categories',
      title: 'Kategoriler',
      icon: 'fas fa-folder',
      items: [
        {
          id: 'category-tree',
          name: 'Kategori Ağacı',
          path: '/categories/tree',
          icon: 'fas fa-sitemap'
        },
        {
          id: 'category-mapping',
          name: 'Kategori Eşleştirme',
          path: '/categories/mapping',
          icon: 'fas fa-link'
        },
        {
          id: 'category-templates',
          name: 'Kategori Şablonları',
          path: '/categories/templates',
          icon: 'fas fa-copy'
        }
      ]
    },
    {
      id: 'tire-specs',
      title: 'Lastik Özellikleri',
      icon: 'fas fa-cog',
      items: [
        {
          id: 'dimensions',
          name: 'Ebatlar',
          path: '/tire-specs/dimensions',
          icon: 'fas fa-ruler-combined'
        },
        {
          id: 'seasons',
          name: 'Mevsim Tipleri',
          path: '/tire-specs/seasons',
          icon: 'fas fa-sun'
        },
        {
          id: 'speed-codes',
          name: 'Hız Kodları',
          path: '/tire-specs/speed-codes',
          icon: 'fas fa-tachometer-alt'
        },
        {
          id: 'load-indexes',
          name: 'Yük Endeksleri',
          path: '/tire-specs/load-indexes',
          icon: 'fas fa-weight'
        },
        {
          id: 'spec-sets',
          name: 'Özellik Setleri',
          path: '/tire-specs/spec-sets',
          icon: 'fas fa-list-alt'
        }
      ]
    },
    {
      id: 'brands',
      title: 'Markalar',
      icon: 'fas fa-trademark',
      items: [
        {
          id: 'brand-management',
          name: 'Marka Yönetimi',
          path: '/brands/management',
          icon: 'fas fa-cogs'
        },
        {
          id: 'brand-categories',
          name: 'Marka-Kategori İlişkileri',
          path: '/brands/categories',
          icon: 'fas fa-th-list'
        }
      ]
    },
    {
      id: 'stock-management',
      title: 'Stok Yönetimi',
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
              path: '/stock/general',
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
              icon: 'fas fa-exclamation'
            }
          ]
        },
        {
          id: 'stock-movements',
          name: 'Stok Hareketleri',
          icon: 'fas fa-exchange-alt',
          items: [
            {
              id: 'in-out',
              name: 'Giriş/Çıkış Kayıtları',
              path: '/stock/movements/in-out',
              icon: 'fas fa-random'
            },
            {
              id: 'transfers',
              name: 'Transfer İşlemleri',
              path: '/stock/movements/transfers',
              icon: 'fas fa-truck'
            },
            {
              id: 'history',
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
              path: '/warehouse/list',
              icon: 'fas fa-list'
            },
            {
              id: 'warehouse-layout',
              name: 'Depo Düzeni',
              path: '/warehouse/layout',
              icon: 'fas fa-th'
            },
            {
              id: 'shelf-system',
              name: 'Raf Sistemi',
              path: '/warehouse/shelf',
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
              path: '/inventory/new',
              icon: 'fas fa-plus'
            },
            {
              id: 'count-history',
              name: 'Sayım Geçmişi',
              path: '/inventory/history',
              icon: 'fas fa-history'
            },
            {
              id: 'count-reports',
              name: 'Sayım Raporları',
              path: '/inventory/reports',
              icon: 'fas fa-file-alt'
            }
          ]
        }
      ]
    },
    {
      id: 'order-management',
      title: 'Sipariş Yönetimi',
      icon: 'fas fa-shopping-cart',
      items: [
        {
          id: 'orders',
          name: 'Siparişler',
          icon: 'fas fa-shopping-cart',
          items: [
            {
              id: 'all-orders',
              name: 'Tüm Siparişler',
              path: '/orders/all',
              icon: 'fas fa-list'
            },
            {
              id: 'pending-orders',
              name: 'Bekleyen Siparişler',
              path: '/orders/pending',
              icon: 'fas fa-clock'
            },
            {
              id: 'awaiting-approval',
              name: 'Onay Bekleyenler',
              path: '/orders/approval',
              icon: 'fas fa-hourglass'
            },
            {
              id: 'completed-orders',
              name: 'Tamamlananlar',
              path: '/orders/completed',
              icon: 'fas fa-check'
            }
          ]
        },
        {
          id: 'shipping',
          name: 'Kargo Yönetimi',
          icon: 'fas fa-truck',
          items: [
            {
              id: 'shipping-integrations',
              name: 'Kargo Entegrasyonları',
              path: '/shipping/integrations',
              icon: 'fas fa-plug'
            },
            {
              id: 'shipping-tracking',
              name: 'Kargo Takibi',
              path: '/shipping/tracking',
              icon: 'fas fa-map-marker-alt'
            },
            {
              id: 'delivery-settings',
              name: 'Teslimat Ayarları',
              path: '/shipping/settings',
              icon: 'fas fa-cog'
            }
          ]
        },
        {
          id: 'returns',
          name: 'İade İşlemleri',
          icon: 'fas fa-undo',
          items: [
            {
              id: 'return-requests',
              name: 'İade Talepleri',
              path: '/returns/requests',
              icon: 'fas fa-inbox'
            },
            {
              id: 'return-approvals',
              name: 'İade Onayları',
              path: '/returns/approvals',
              icon: 'fas fa-check-circle'
            },
            {
              id: 'return-reports',
              name: 'İade Raporları',
              path: '/returns/reports',
              icon: 'fas fa-chart-bar'
            }
          ]
        }
      ]
    },
    {
      id: 'account-management',
      title: 'Cari Hesap Yönetimi',
      icon: 'fas fa-users',
      items: [
        {
          id: 'customers',
          name: 'Müşteriler',
          icon: 'fas fa-user',
          items: [
            {
              id: 'customer-list',
              name: 'Müşteri Listesi',
              path: '/customers/list',
              icon: 'fas fa-list'
            },
            {
              id: 'customer-groups',
              name: 'Müşteri Grupları',
              path: '/customers/groups',
              icon: 'fas fa-users'
            },
            {
              id: 'customer-cards',
              name: 'Müşteri Kartları',
              path: '/customers/cards',
              icon: 'fas fa-id-card'
            }
          ]
        },
        {
          id: 'suppliers',
          name: 'Tedarikçiler',
          icon: 'fas fa-truck',
          items: [
            {
              id: 'supplier-list',
              name: 'Tedarikçi Listesi',
              path: '/suppliers/list',
              icon: 'fas fa-list'
            },
            {
              id: 'supplier-evaluation',
              name: 'Tedarikçi Değerlendirme',
              path: '/suppliers/evaluation',
              icon: 'fas fa-star'
            },
            {
              id: 'order-history',
              name: 'Sipariş Geçmişi',
              path: '/suppliers/orders',
              icon: 'fas fa-history'
            }
          ]
        },
        {
          id: 'dealers',
          name: 'Bayiler',
          icon: 'fas fa-store',
          items: [
            {
              id: 'dealer-list',
              name: 'Bayi Listesi',
              path: '/dealers/list',
              icon: 'fas fa-list'
            },
            {
              id: 'dealer-prices',
              name: 'Bayi Özel Fiyatları',
              path: '/dealers/prices',
              icon: 'fas fa-tag'
            },
            {
              id: 'dealer-reports',
              name: 'Bayi Raporları',
              path: '/dealers/reports',
              icon: 'fas fa-chart-bar'
            }
          ]
        },
        {
          id: 'account-operations',
          name: 'Cari Hesap İşlemleri',
          icon: 'fas fa-file-invoice-dollar',
          items: [
            {
              id: 'debt-credit',
              name: 'Borç/Alacak Takibi',
              path: '/accounts/debt-credit',
              icon: 'fas fa-balance-scale'
            },
            {
              id: 'payments',
              name: 'Ödeme İşlemleri',
              path: '/accounts/payments',
              icon: 'fas fa-money-bill'
            },
            {
              id: 'account-statements',
              name: 'Hesap Ekstreleri',
              path: '/accounts/statements',
              icon: 'fas fa-file-alt'
            }
          ]
        }
      ]
    },
    {
      id: 'pricing',
      title: 'Fiyatlandırma',
      icon: 'fas fa-tag',
      items: [
        {
          id: 'price-lists',
          name: 'Fiyat Listeleri',
          icon: 'fas fa-list',
          items: [
            {
              id: 'retail-prices',
              name: 'Perakende Fiyatları',
              path: '/pricing/retail',
              icon: 'fas fa-tag'
            },
            {
              id: 'dealer-prices',
              name: 'Bayi Fiyatları',
              path: '/pricing/dealer',
              icon: 'fas fa-tags'
            },
            {
              id: 'special-prices',
              name: 'Özel Fiyatlar',
              path: '/pricing/special',
              icon: 'fas fa-star'
            }
          ]
        },
        {
          id: 'campaigns',
          name: 'Kampanyalar',
          icon: 'fas fa-percentage',
          items: [
            {
              id: 'active-campaigns',
              name: 'Aktif Kampanyalar',
              path: '/campaigns/active',
              icon: 'fas fa-check'
            },
            {
              id: 'create-campaign',
              name: 'Kampanya Oluştur',
              path: '/campaigns/create',
              icon: 'fas fa-plus'
            },
            {
              id: 'campaign-history',
              name: 'Kampanya Geçmişi',
              path: '/campaigns/history',
              icon: 'fas fa-history'
            }
          ]
        },
        {
          id: 'price-update',
          name: 'Fiyat Güncelleme',
          icon: 'fas fa-sync',
          items: [
            {
              id: 'bulk-update',
              name: 'Toplu Güncelleme',
              path: '/price-update/bulk',
              icon: 'fas fa-tasks'
            },
            {
              id: 'currency-update',
              name: 'Kur Bazlı Güncelleme',
              path: '/price-update/currency',
              icon: 'fas fa-dollar-sign'
            },
            {
              id: 'update-history',
              name: 'Güncelleme Geçmişi',
              path: '/price-update/history',
              icon: 'fas fa-history'
            }
          ]
        }
      ]
    },
    {
      id: 'ecommerce',
      title: 'E-Ticaret',
      icon: 'fas fa-shopping-bag',
      items: [
        {
          id: 'woocommerce',
          name: 'WooCommerce',
          icon: 'fab fa-wordpress',
          items: [
            {
              id: 'product-sync',
              name: 'Ürün Senkronizasyonu',
              path: '/woocommerce/product-sync',
              icon: 'fas fa-sync'
            },
            {
              id: 'stock-sync',
              name: 'Stok Senkronizasyonu',
              path: '/woocommerce/stock-sync',
              icon: 'fas fa-boxes'
            },
            {
              id: 'order-sync',
              name: 'Sipariş Senkronizasyonu',
              path: '/woocommerce/order-sync',
              icon: 'fas fa-shopping-cart'
            }
          ]
        },
        {
          id: 'marketplaces',
          name: 'Pazaryeri Entegrasyonları',
          icon: 'fas fa-store',
          items: [
            {
              id: 'n11',
              name: 'N11',
              path: '/marketplaces/n11',
              icon: 'fas fa-shopping-bag'
            },
            {
              id: 'trendyol',
              name: 'Trendyol',
              path: '/marketplaces/trendyol',
              icon: 'fas fa-shopping-bag'
            },
            {
              id: 'hepsiburada',
              name: 'HepsiBurada',
              path: '/marketplaces/hepsiburada',
              icon: 'fas fa-shopping-bag'
            },
            {
              id: 'gittigidiyor',
              name: 'GittiGidiyor',
              path: '/marketplaces/gittigidiyor',
              icon: 'fas fa-shopping-bag'
            }
          ]
        },
        {
          id: 'ecommerce-settings',
          name: 'E-Ticaret Ayarları',
          icon: 'fas fa-cog',
          items: [
            {
              id: 'api-settings',
              name: 'API Ayarları',
              path: '/ecommerce/api-settings',
              icon: 'fas fa-key'
            },
            {
              id: 'sync-rules',
              name: 'Senkronizasyon Kuralları',
              path: '/ecommerce/sync-rules',
              icon: 'fas fa-list-ol'
            },
            {
              id: 'auto-operations',
              name: 'Otomatik İşlemler',
              path: '/ecommerce/auto-operations',
              icon: 'fas fa-robot'
            }
          ]
        }
      ]
    },
    {
      id: 'reports',
      title: 'Raporlar',
      icon: 'fas fa-chart-bar',
      items: [
        {
          id: 'sales-reports',
          name: 'Satış Raporları',
          icon: 'fas fa-chart-line',
          items: [
            {
              id: 'daily-sales',
              name: 'Günlük Satışlar',
              path: '/reports/sales/daily',
              icon: 'fas fa-calendar-day'
            },
            {
              id: 'product-sales',
              name: 'Ürün Bazlı Satışlar',
              path: '/reports/sales/products',
              icon: 'fas fa-box'
            },
            {
              id: 'channel-sales',
              name: 'Kanal Bazlı Satışlar',
              path: '/reports/sales/channels',
              icon: 'fas fa-store'
            }
          ]
        },
        {
          id: 'stock-reports',
          name: 'Stok Raporları',
          icon: 'fas fa-boxes',
          items: [
            {
              id: 'stock-status',
              name: 'Stok Durumu',
              path: '/reports/stock/status',
              icon: 'fas fa-warehouse'
            },
            {
              id: 'stock-movements',
              name: 'Stok Hareketleri',
              path: '/reports/stock/movements',
              icon: 'fas fa-exchange-alt'
            },
            {
              id: 'min-stock',
              name: 'Minimum Stok',
              path: '/reports/stock/minimum',
              icon: 'fas fa-exclamation'
            }
          ]
        },
        {
          id: 'financial-reports',
          name: 'Finansal Raporlar',
          icon: 'fas fa-file-invoice-dollar',
          items: [
            {
              id: 'income-expense',
              name: 'Gelir/Gider',
              path: '/reports/financial/income-expense',
              icon: 'fas fa-balance-scale'
            },
            {
              id: 'profit-loss',
              name: 'Kâr/Zarar Analizi',
              path: '/reports/financial/profit-loss',
              icon: 'fas fa-chart-pie'
            },
            {
              id: 'collection-reports',
              name: 'Tahsilat Raporları',
              path: '/reports/financial/collections',
              icon: 'fas fa-money-bill'
            }
          ]
        },
        {
          id: 'analysis-reports',
          name: 'Analiz Raporları',
          icon: 'fas fa-chart-pie',
          items: [
            {
              id: 'sales-trends',
              name: 'Satış Trendleri',
              path: '/reports/analysis/sales-trends',
              icon: 'fas fa-chart-line'
            },
            {
              id: 'product-performance',
              name: 'Ürün Performansı',
              path: '/reports/analysis/product-performance',
              icon: 'fas fa-star'
            },
            {
              id: 'customer-analysis',
              name: 'Müşteri Analizleri',
              path: '/reports/analysis/customer',
              icon: 'fas fa-users'
            }
          ]
        }
      ]
    },
    {
      id: 'settings',
      title: 'Ayarlar',
      icon: 'fas fa-cog',
      items: [
        {
          id: 'system-settings',
          name: 'Sistem Ayarları',
          icon: 'fas fa-cogs',
          items: [
            {
              id: 'general-settings',
              name: 'Genel Ayarlar',
              path: '/settings/system/general',
              icon: 'fas fa-sliders-h'
            },
            {
              id: 'user-management',
              name: 'Kullanıcı Yönetimi',
              path: '/settings/system/users',
              icon: 'fas fa-users-cog'
            },
            {
              id: 'roles-permissions',
              name: 'Rol ve İzinler',
              path: '/settings/system/roles',
              icon: 'fas fa-user-shield'
            }
          ]
        },
        {
          id: 'integration-settings',
          name: 'Entegrasyon Ayarları',
          icon: 'fas fa-plug',
          items: [
            {
              id: 'wolvox-connection',
              name: 'Wolvox Bağlantısı',
              path: '/settings/integration/wolvox',
              icon: 'fas fa-link'
            },
            {
              id: 'woocommerce-settings',
              name: 'WooCommerce Ayarları',
              path: '/settings/integration/woocommerce',
              icon: 'fab fa-wordpress'
            },
            {
              id: 'api-configuration',
              name: 'API Yapılandırması',
              path: '/settings/integration/api',
              icon: 'fas fa-code'
            }
          ]
        },
        {
          id: 'data-management',
          name: 'Veri Yönetimi',
          icon: 'fas fa-database',
          items: [
            {
              id: 'backup',
              name: 'Yedekleme',
              path: '/settings/data/backup',
              icon: 'fas fa-save'
            },
            {
              id: 'restore',
              name: 'Geri Yükleme',
              path: '/settings/data/restore',
              icon: 'fas fa-undo'
            },
            {
              id: 'data-cleanup',
              name: 'Veri Temizleme',
              path: '/settings/data/cleanup',
              icon: 'fas fa-broom'
            }
          ]
        },
        {
          id: 'notification-settings',
          name: 'Bildirim Ayarları',
          icon: 'fas fa-bell',
          items: [
            {
              id: 'email-notifications',
              name: 'E-posta Bildirimleri',
              path: '/settings/notifications/email',
              icon: 'fas fa-envelope'
            },
            {
              id: 'sms-notifications',
              name: 'SMS Bildirimleri',
              path: '/settings/notifications/sms',
              icon: 'fas fa-sms'
            },
            {
              id: 'system-notifications',
              name: 'Sistem Bildirimleri',
              path: '/settings/notifications/system',
              icon: 'fas fa-desktop'
            }
          ]
        }
      ]
    },
    {
      id: 'help-support',
      title: 'Yardım & Destek',
      icon: 'fas fa-question-circle',
      items: [
        {
          id: 'user-guide',
          name: 'Kullanım Kılavuzu',
          path: '/help/guide',
          icon: 'fas fa-book'
        },
        {
          id: 'faq',
          name: 'Sık Sorulan Sorular',
          path: '/help/faq',
          icon: 'fas fa-question'
        },
        {
          id: 'technical-support',
          name: 'Teknik Destek',
          path: '/help/support',
          icon: 'fas fa-headset'
        },
        {
          id: 'operation-history',
          name: 'İşlem Geçmişi',
          path: '/help/history',
          icon: 'fas fa-history'
        }
      ]
    }
  ]
}; 