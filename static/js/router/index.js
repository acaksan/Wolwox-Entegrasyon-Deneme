const Dashboard = {
    template: /* html */`
        <div class="p-6">
            <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
            <p>Yükleniyor...</p>
        </div>
    `
}

// Lazy loading için bileşenleri dinamik olarak import edelim
const routes = [
    {
        path: '/',
        name: 'Dashboard',
        component: () => import('../pages/Dashboard.js')
    },
    {
        path: '/products/list',
        name: 'Ürün Listesi',
        component: () => import('../pages/products/ProductList.js')
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../pages/NotFound.js')
    }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
}) 