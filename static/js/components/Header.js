export default {
    name: 'Header',
    template: `
        <header class="bg-white shadow-sm p-4">
            <div class="flex justify-between items-center">
                <div>
                    <h2 class="text-xl font-semibold">{{ $route.name || 'Dashboard' }}</h2>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-500">Son Senkronizasyon: Hiç</span>
                    <button @click="syncAll" 
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                        <i class="fas fa-sync mr-2"></i> Senkronize Et
                    </button>
                </div>
            </div>
        </header>
    `,
    methods: {
        syncAll() {
            // Senkronizasyon işlemi burada yapılacak
            console.log('Senkronizasyon başlatıldı')
        }
    }
} 