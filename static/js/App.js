export default {
    template: `
        <div class="min-h-screen bg-gray-100">
            <Sidebar />
            <div class="ml-64">
                <Header />
                <main class="p-8">
                    <router-view></router-view>
                </main>
            </div>
        </div>
    `,
    components: {
        Sidebar: () => import('./components/Sidebar.js'),
        Header: () => import('./components/Header.js')
    }
} 