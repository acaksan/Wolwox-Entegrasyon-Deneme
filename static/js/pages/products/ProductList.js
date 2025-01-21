export default {
    name: 'ProductList',
    data() {
        return {
            products: [],
            loading: true,
            filters: {
                search: '',
                category: '',
                brand: '',
                status: ''
            },
            pagination: {
                currentPage: 1,
                totalPages: 1,
                perPage: 10
            }
        }
    },
    template: /* html */`
        <div class="p-6">
            <div class="flex justify-between items-center mb-6">
                <h1 class="text-2xl font-bold text-gray-800">Ürün Listesi</h1>
                <button class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center">
                    <i class="fas fa-plus mr-2"></i>
                    Yeni Ürün Ekle
                </button>
            </div>

            <!-- Filtreler -->
            <div class="bg-white rounded-lg shadow p-4 mb-6">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Arama</label>
                        <input 
                            type="text" 
                            v-model="filters.search"
                            placeholder="Ürün ara..."
                            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Kategori</label>
                        <select 
                            v-model="filters.category"
                            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Tümü</option>
                            <option value="summer">Yaz Lastiği</option>
                            <option value="winter">Kış Lastiği</option>
                            <option value="allseason">4 Mevsim</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Marka</label>
                        <select 
                            v-model="filters.brand"
                            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Tümü</option>
                            <option value="michelin">Michelin</option>
                            <option value="goodyear">Goodyear</option>
                            <option value="bridgestone">Bridgestone</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Durum</label>
                        <select 
                            v-model="filters.status"
                            class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Tümü</option>
                            <option value="active">Aktif</option>
                            <option value="inactive">Pasif</option>
                            <option value="outofstock">Stok Dışı</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Ürün Tablosu -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ürün</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stok Kodu</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategori</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stok</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fiyat</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Durum</th>
                            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">İşlemler</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-if="loading">
                            <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                                Yükleniyor...
                            </td>
                        </tr>
                        <tr v-else v-for="product in products" :key="product.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="h-10 w-10 flex-shrink-0">
                                        <img :src="product.image" class="h-10 w-10 rounded-full">
                                    </div>
                                    <div class="ml-4">
                                        <div class="text-sm font-medium text-gray-900">{{ product.name }}</div>
                                        <div class="text-sm text-gray-500">{{ product.brand }}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.sku }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.category }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ product.stock }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">₺{{ product.price }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span :class="{
                                    'px-2 py-1 text-xs font-medium rounded-full': true,
                                    'bg-green-100 text-green-800': product.status === 'active',
                                    'bg-red-100 text-red-800': product.status === 'inactive',
                                    'bg-yellow-100 text-yellow-800': product.status === 'outofstock'
                                }">
                                    {{ product.statusText }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button class="text-blue-600 hover:text-blue-900 mr-3">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="text-red-600 hover:text-red-900">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <!-- Pagination -->
                <div class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
                    <div class="flex items-center justify-between">
                        <div class="text-sm text-gray-700">
                            Toplam <span class="font-medium">{{ products.length }}</span> ürün
                        </div>
                        <div class="flex-1 flex justify-center">
                            <button 
                                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 mx-1"
                                :disabled="pagination.currentPage === 1"
                            >
                                Önceki
                            </button>
                            <button 
                                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 mx-1"
                                :disabled="pagination.currentPage === pagination.totalPages"
                            >
                                Sonraki
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    mounted() {
        // API'den ürün verilerini çekme simülasyonu
        setTimeout(() => {
            this.products = [
                {
                    id: 1,
                    name: '205/55R16 91H',
                    brand: 'Michelin',
                    sku: 'MCH-205-55-16',
                    category: 'Yaz Lastiği',
                    stock: 45,
                    price: '1.250,00',
                    status: 'active',
                    statusText: 'Aktif',
                    image: 'https://via.placeholder.com/40'
                },
                {
                    id: 2,
                    name: '195/65R15 91T',
                    brand: 'Goodyear',
                    sku: 'GDY-195-65-15',
                    category: 'Kış Lastiği',
                    stock: 12,
                    price: '950,00',
                    status: 'outofstock',
                    statusText: 'Stok Az',
                    image: 'https://via.placeholder.com/40'
                },
                {
                    id: 3,
                    name: '225/45R17 94W',
                    brand: 'Bridgestone',
                    sku: 'BRD-225-45-17',
                    category: '4 Mevsim',
                    stock: 0,
                    price: '1.450,00',
                    status: 'inactive',
                    statusText: 'Pasif',
                    image: 'https://via.placeholder.com/40'
                },
                {
                    id: 4,
                    name: '215/50R17 91V',
                    brand: 'Michelin',
                    sku: 'MCH-215-50-17',
                    category: 'Yaz Lastiği',
                    stock: 28,
                    price: '1.350,00',
                    status: 'active',
                    statusText: 'Aktif',
                    image: 'https://via.placeholder.com/40'
                },
                {
                    id: 5,
                    name: '185/65R15 88T',
                    brand: 'Goodyear',
                    sku: 'GDY-185-65-15',
                    category: 'Kış Lastiği',
                    stock: 8,
                    price: '850,00',
                    status: 'outofstock',
                    statusText: 'Stok Az',
                    image: 'https://via.placeholder.com/40'
                }
            ]
            this.loading = false
        }, 1000)
    }
} 