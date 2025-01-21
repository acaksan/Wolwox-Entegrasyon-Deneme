export const menuConfig = {
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
                    path: '/',
                    icon: 'fas fa-chart-line',
                    active: true,
                    status: 'development'
                }
            ]
        }
        // Diğer menü grupları buraya eklenecek
    ]
} 