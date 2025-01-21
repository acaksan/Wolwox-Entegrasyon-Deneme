const { ref, computed } = Vue

export default {
    name: 'Sidebar',
    setup() {
        const isCollapsed = ref(false)
        const hoveredGroup = ref(null)
        const activeItem = ref(null)

        const sidebarClass = computed(() => ({
            'w-64': !isCollapsed.value,
            'w-20': isCollapsed.value,
            'transition-all duration-300': true
        }))

        const toggleSidebar = () => {
            isCollapsed.value = !isCollapsed.value
        }

        return {
            isCollapsed,
            hoveredGroup,
            activeItem,
            sidebarClass,
            toggleSidebar
        }
    },
    template: `
        <nav :class="sidebarClass" 
             class="fixed top-0 left-0 h-full bg-white shadow-lg z-50">
            <!-- Logo ve Başlık -->
            <div class="flex items-center justify-between p-4 border-b">
                <div class="flex items-center space-x-3" v-show="!isCollapsed">
                    <img src="/static/img/logo.png" class="h-8 w-8" alt="Logo">
                    <div>
                        <h1 class="text-xl font-bold text-gray-800">Lastik Entegrasyon</h1>
                        <p class="text-sm text-gray-500">Wolvox - WooCommerce</p>
                    </div>
                </div>
                <button @click="toggleSidebar" 
                        class="p-2 rounded-lg hover:bg-gray-100 text-gray-500">
                    <i :class="isCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
                </button>
            </div>

            <!-- Menü İçeriği -->
            <div class="overflow-y-auto h-[calc(100vh-5rem)] pb-20 custom-scrollbar">
                <template v-for="group in menu.items" :key="group.id">
                    <div class="border-b border-gray-100"
                         @mouseenter="hoveredGroup = group.id"
                         @mouseleave="hoveredGroup = null">
                        <!-- Grup Başlığı -->
                        <div class="p-4 text-sm font-medium text-gray-500 bg-gray-50 flex items-center justify-between">
                            <span v-show="!isCollapsed">{{ group.title }}</span>
                            <i :class="group.icon" v-show="isCollapsed"></i>
                            <span v-if="group.badge" 
                                  :class="[
                                    'text-xs px-2 py-1 rounded-full',
                                    `bg-${group.badge.type}-100 text-${group.badge.type}-800`
                                  ]">
                                {{ group.badge.text }}
                            </span>
                        </div>

                        <!-- Grup Öğeleri -->
                        <template v-for="item in group.items" :key="item.id">
                            <!-- Alt menüsü olan öğeler -->
                            <template v-if="item.items">
                                <div class="relative group">
                                    <div class="p-3 pl-6 flex items-center justify-between hover:bg-gray-50 cursor-pointer"
                                         :class="{'bg-blue-50': activeItem === item.id}">
                                        <div class="flex items-center space-x-3">
                                            <i :class="[item.icon, 'w-6 text-gray-500']"></i>
                                            <span v-show="!isCollapsed">{{ item.name }}</span>
                                        </div>
                                        <i class="fas fa-chevron-right text-xs" v-show="!isCollapsed"></i>
                                    </div>

                                    <!-- Alt Menü -->
                                    <div class="absolute left-full top-0 ml-2 w-64 bg-white shadow-lg rounded-lg overflow-hidden transform scale-0 group-hover:scale-100 transition-transform origin-left">
                                        <div class="py-2">
                                            <template v-for="subItem in item.items" :key="subItem.id">
                                                <a :href="subItem.path"
                                                   class="block px-4 py-2 hover:bg-gray-50 flex items-center justify-between">
                                                    <div class="flex items-center space-x-3">
                                                        <i :class="[subItem.icon, 'w-6 text-gray-500']"></i>
                                                        <span>{{ subItem.name }}</span>
                                                    </div>
                                                    <div class="flex items-center space-x-2">
                                                        <span v-if="subItem.counter" 
                                                              class="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                                                            {{ subItem.counter }}
                                                        </span>
                                                        <span v-if="subItem.badge" 
                                                              :class="[
                                                                'text-xs px-2 py-1 rounded-full',
                                                                `bg-${subItem.badge.type}-100 text-${subItem.badge.type}-800`
                                                              ]">
                                                            {{ subItem.badge.text }}
                                                        </span>
                                                    </div>
                                                </a>
                                            </template>
                                        </div>
                                    </div>
                                </div>
                            </template>

                            <!-- Alt menüsü olmayan öğeler -->
                            <template v-else>
                                <a :href="item.path"
                                   class="block p-3 pl-6 hover:bg-gray-50 flex items-center justify-between"
                                   :class="{'bg-blue-50': activeItem === item.id}">
                                    <div class="flex items-center space-x-3">
                                        <i :class="[item.icon, 'w-6 text-gray-500']"></i>
                                        <span v-show="!isCollapsed">{{ item.name }}</span>
                                    </div>
                                    <template v-if="!isCollapsed">
                                        <span v-if="item.counter" 
                                              class="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                                            {{ item.counter }}
                                        </span>
                                        <span v-if="item.badge" 
                                              :class="[
                                                'text-xs px-2 py-1 rounded-full',
                                                `bg-${item.badge.type}-100 text-${item.badge.type}-800`
                                              ]">
                                            {{ item.badge.text }}
                                        </span>
                                    </template>
                                </a>
                            </template>
                        </template>
                    </div>
                </template>
            </div>
        </nav>
    `
} 