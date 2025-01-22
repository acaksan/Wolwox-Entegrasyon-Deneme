const { defineComponent } = Vue

export default defineComponent({
    name: 'DefaultLayout',
    components: {
        Sidebar: () => import('../components/Sidebar.js')
    },
    template: /* html */`
        <div class="min-h-screen bg-gray-100">
            <Sidebar />
            <div class="ml-64">
                <main class="p-8">
                    <router-view></router-view>
                </main>
            </div>
        </div>
    `
}) 