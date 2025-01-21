export const menuItems = [
  {
    title: 'Ana Menü',
    items: [
      {
        name: 'Dashboard',
        path: '/',
        icon: 'fas fa-home'
      }
    ]
  },
  {
    title: 'Ürün Yönetimi',
    items: [
      {
        name: 'Ürünler',
        path: '/products',
        icon: 'fas fa-box'
      },
      {
        name: 'Toplu Ürün İşlemleri',
        path: '/products/bulk',
        icon: 'fas fa-boxes'
      }
      // ... diğer menü öğeleri
    ]
  },
  {
    title: 'Ayarlar',
    items: [
      {
        name: 'Bağlantı Testi',
        path: '/settings/connection-test',
        icon: 'fas fa-plug'
      },
      // ... diğer ayarlar
    ]
  }
  // ... diğer menü grupları
] 