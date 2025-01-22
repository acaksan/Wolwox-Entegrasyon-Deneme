export const menuConfig = {
  items: [
    {
      id: 'wolvox',
      title: 'Akınsoft Wolvox Entegrasyon',
      icon: 'fas fa-database',
      items: [
        {
          id: 'wolvox-connection',
          name: 'Bağlantı Ayarları',
          path: '/wolvox/connection',
          icon: 'fas fa-plug'
        },
        {
          id: 'wolvox-products',
          name: 'Ürün Senkronizasyonu',
          path: '/wolvox/products',
          icon: 'fas fa-box'
        },
        {
          id: 'wolvox-stock',
          name: 'Stok Senkronizasyonu',
          path: '/wolvox/stock',
          icon: 'fas fa-boxes'
        },
        {
          id: 'wolvox-orders',
          name: 'Sipariş Senkronizasyonu',
          path: '/wolvox/orders',
          icon: 'fas fa-shopping-cart'
        }
      ]
    },
    {
      id: 'woocommerce',
      title: 'WooCommerce',
      icon: 'fab fa-wordpress',
      items: [
        {
          id: 'woo-settings',
          name: 'WooCommerce Ayarları',
          path: '/woocommerce/settings',
          icon: 'fas fa-cog'
        },
        {
          id: 'woo-products',
          name: 'Ürün Aktarımı',
          path: '/woocommerce/products',
          icon: 'fas fa-sync'
        },
        {
          id: 'woo-stock',
          name: 'Stok Aktarımı',
          path: '/woocommerce/stock',
          icon: 'fas fa-boxes'
        },
        {
          id: 'woo-orders',
          name: 'Sipariş Takibi',
          path: '/woocommerce/orders',
          icon: 'fas fa-shopping-cart'
        }
      ]
    },
    {
      id: 'settings',
      title: 'Ayarlar',
      icon: 'fas fa-cog',
      items: [
        {
          id: 'general-settings',
          name: 'Genel Ayarlar',
          path: '/settings/general',
          icon: 'fas fa-sliders-h'
        },
        {
          id: 'api-settings',
          name: 'API Ayarları',
          path: '/settings/api',
          icon: 'fas fa-key'
        },
        {
          id: 'system-logs',
          name: 'Sistem Logları',
          path: '/settings/logs',
          icon: 'fas fa-clipboard-list'
        }
      ]
    }
  ]
}; 