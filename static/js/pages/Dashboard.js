export default {
    name: 'Dashboard',
    data() {
        return {
            stats: {
                orders: {
                    total: 0,
                    pending: 0,
                    completed: 0
                },
                revenue: {
                    daily: 0,
                    monthly: 0,
                    annual: 0
                },
                stock: {
                    total: 0,
                    critical: 0,
                    outOfStock: 0
                }
            }
        }
    },
    template: /* html */`
        <div class="p-6">
            <div class="mb-8">
                <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
                <p class="text-gray-600">Hoş geldiniz, işte genel durum özeti</p>
            </div>

            <!-- İstatistik Kartları -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Sipariş İstatistikleri -->
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Siparişler</h3>
                        <i class="fas fa-shopping-cart text-blue-500"></i>
                    </div>
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Toplam Sipariş</span>
                            <span class="font-semibold">{{ stats.orders.total }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Bekleyen</span>
                            <span class="font-semibold text-yellow-500">{{ stats.orders.pending }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Tamamlanan</span>
                            <span class="font-semibold text-green-500">{{ stats.orders.completed }}</span>
                        </div>
                    </div>
                </div>

                <!-- Gelir İstatistikleri -->
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Gelir</h3>
                        <i class="fas fa-chart-line text-green-500"></i>
                    </div>
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Günlük</span>
                            <span class="font-semibold">₺{{ stats.revenue.daily.toLocaleString() }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Aylık</span>
                            <span class="font-semibold">₺{{ stats.revenue.monthly.toLocaleString() }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Yıllık</span>
                            <span class="font-semibold">₺{{ stats.revenue.annual.toLocaleString() }}</span>
                        </div>
                    </div>
                </div>

                <!-- Stok Durumu -->
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Stok Durumu</h3>
                        <i class="fas fa-boxes text-purple-500"></i>
                    </div>
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span class="text-gray-600">Toplam Ürün</span>
                            <span class="font-semibold">{{ stats.stock.total }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Kritik Seviye</span>
                            <span class="font-semibold text-orange-500">{{ stats.stock.critical }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-600">Tükenen</span>
                            <span class="font-semibold text-red-500">{{ stats.stock.outOfStock }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Hızlı Erişim Butonları -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <button class="p-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center justify-center">
                    <i class="fas fa-plus-circle mr-2"></i>
                    Yeni Sipariş
                </button>
                <button class="p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center justify-center">
                    <i class="fas fa-box mr-2"></i>
                    Ürün Ekle
                </button>
                <button class="p-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600 flex items-center justify-center">
                    <i class="fas fa-sync mr-2"></i>
                    Stok Güncelle
                </button>
                <button class="p-4 bg-orange-500 text-white rounded-lg hover:bg-orange-600 flex items-center justify-center">
                    <i class="fas fa-file-alt mr-2"></i>
                    Rapor Oluştur
                </button>
            </div>

            <!-- Son Aktiviteler -->
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Son Aktiviteler</h3>
                <div class="text-gray-500">
                    <p>Yapım aşamasında...</p>
                </div>
            </div>
        </div>
    `,
    mounted() {
        // API'den verileri çekme simülasyonu
        setTimeout(() => {
            this.stats = {
                orders: {
                    total: 150,
                    pending: 45,
                    completed: 105
                },
                revenue: {
                    daily: 12500,
                    monthly: 375000,
                    annual: 4500000
                },
                stock: {
                    total: 1250,
                    critical: 85,
                    outOfStock: 23
                }
            }
        }, 1000)
    }
} 