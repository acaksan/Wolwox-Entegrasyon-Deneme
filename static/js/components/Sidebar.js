const { defineComponent } = Vue

export default defineComponent({
    name: 'Sidebar',
    data() {
        return {
            menu: {
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
                            },
                            {
                                id: 'sales-stats',
                                name: 'Satış İstatistikleri',
                                path: '/dashboard/sales',
                                icon: 'fas fa-chart-bar',
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
                                path: '/products/list',
                                icon: 'fas fa-list',
                                active: true,
                                status: 'development'
                            }
                        ]
                    }
                ]
            }
        }
    },
    template: /* html */`
        <nav class="fixed top-0 left-0 h-full w-64 bg-white shadow-lg overflow-y-auto">
            <div class="p-4 border-b">
                <h1 class="text-xl font-bold text-gray-800">Lastik Entegrasyon</h1>
                <p class="text-sm text-gray-500">Wolvox - WooCommerce</p>
            </div>
            
            <div class="overflow-y-auto h-full pb-20">
                <template v-for="group in menu.items" :key="group.id">
                    <div class="border-t">
                        <div class="p-4 text-sm font-medium text-gray-500 bg-gray-50">
                            {{ group.title }}
                        </div>
                        <template v-for="item in group.items" :key="item.id">
                            <!-- Ana menü öğesi -->
                            <template v-if="!item.items">
                                <router-link :to="item.path" 
                                    class="block p-4 hover:bg-gray-100 flex items-center">
                                    <i :class="item.icon + ' w-6 text-gray-500'"></i>
                                    <span class="ml-2">{{ item.name }}</span>
                                    <span v-if="item.status === 'development'"
                                        class="ml-auto text-xs bg-yellow-500 text-white px-2 py-1 rounded">
                                        Yapım Aşamasında
                                    </span>
                                </router-link>
                            </template>
                            
                            <!-- Alt menü öğeleri olan ana menü -->
                            <template v-else>
                                <div class="pl-4">
                                    <div class="p-3 text-sm font-medium text-gray-700 flex items-center">
                                        <i :class="item.icon + ' w-6 text-gray-500'"></i>
                                        <span class="ml-2">{{ item.name }}</span>
                                    </div>
                                    <template v-for="subItem in item.items" :key="subItem.id">
                                        <router-link :to="subItem.path"
                                            class="block p-3 pl-12 hover:bg-gray-100 flex items-center">
                                            <i :class="subItem.icon + ' w-6 text-gray-500'"></i>
                                            <span class="ml-2">{{ subItem.name }}</span>
                                            <span v-if="subItem.status === 'development'"
                                                class="ml-auto text-xs bg-yellow-500 text-white px-2 py-1 rounded">
                                                Yapım Aşamasında
                                            </span>
                                        </router-link>
                                    </template>
                                </div>
                            </template>
                        </template>
                    </div>
                </template>
            </div>
        </nav>
    `
}) 