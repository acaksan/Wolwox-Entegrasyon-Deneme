import { menuConfig } from './config/menu-structure.js'

const app = Vue.createApp({
    data() {
        return {
            menu: menuConfig
        }
    },
    template: `
        <div class="min-h-screen bg-gray-100">
            <nav class="fixed top-0 left-0 h-full w-64 bg-white shadow-lg">
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
                                <!-- Alt menüsü olan öğeler -->
                                <template v-if="item.items">
                                    <div class="pl-4">
                                        <div class="p-3 text-sm font-medium text-gray-700 flex items-center">
                                            <i :class="item.icon + ' w-6 text-gray-500'"></i>
                                            <span class="ml-2">{{ item.name }}</span>
                                        </div>
                                        <template v-for="subItem in item.items" :key="subItem.id">
                                            <a :href="subItem.path"
                                                class="block p-3 pl-12 hover:bg-gray-100 flex items-center">
                                                <i :class="subItem.icon + ' w-6 text-gray-500'"></i>
                                                <span class="ml-2">{{ subItem.name }}</span>
                                                <span v-if="subItem.status === 'development'"
                                                    class="ml-auto text-xs bg-yellow-500 text-white px-2 py-1 rounded">
                                                    Yapım Aşamasında
                                                </span>
                                            </a>
                                        </template>
                                    </div>
                                </template>
                                
                                <!-- Alt menüsü olmayan öğeler -->
                                <template v-else>
                                    <a :href="item.path" 
                                        class="block p-4 hover:bg-gray-100 flex items-center">
                                        <i :class="item.icon + ' w-6 text-gray-500'"></i>
                                        <span class="ml-2">{{ item.name }}</span>
                                        <span v-if="item.status === 'development'"
                                            class="ml-auto text-xs bg-yellow-500 text-white px-2 py-1 rounded">
                                            Yapım Aşamasında
                                        </span>
                                    </a>
                                </template>
                            </template>
                        </div>
                    </template>
                </div>
            </nav>

            <main class="ml-64 p-8">
                <router-view></router-view>
            </main>
        </div>
    `
})

app.mount('#app') 