export const menuConfig = {
    items: [
        {
            id: 'dashboard',
            title: 'DASHBOARD',
            icon: 'fas fa-home',
            items: [
                {
                    id: 'overview',
                    name: 'Genel Bakış',
                    path: '/',
                    icon: 'fas fa-chart-line',
                    status: 'development'
                }
            ]
        },
        {
            id: 'products',
            title: 'ÜRÜN YÖNETİMİ',
            icon: 'fas fa-box',
            items: [
                {
                    id: 'product-list',
                    name: 'Ürün Listesi',
                    path: '/products',
                    icon: 'fas fa-list',
                    status: 'development'
                }
            ]
        }
    ]
} 