export default {
    template: `
        <div class="space-y-6">
            <h1 class="text-2xl font-bold">Bağlantı Testi</h1>

            <!-- Wolvox Testi -->
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Wolvox Bağlantısı</h2>
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div v-for="(value, key) in wolvox" :key="key">
                        <label class="block text-sm font-medium text-gray-700">{{ key }}</label>
                        <input v-model="wolvox[key]" 
                               :type="key === 'password' ? 'password' : 'text'"
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                    </div>
                </div>
                <button @click="testWolvox" 
                        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Test Et
                </button>
                <span v-if="wolvoxMessage" 
                      :class="{'text-green-500': wolvoxStatus, 'text-red-500': !wolvoxStatus}"
                      class="ml-4">
                    {{ wolvoxMessage }}
                </span>
            </div>

            <!-- WooCommerce Testi -->
            <div class="bg-white p-6 rounded-lg shadow">
                <!-- Benzer yapı -->
            </div>
        </div>
    `,
    data() {
        return {
            wolvox: {
                host: 'localhost',
                database: 'D:\\AKINSOFT\\Wolvox8\\Database_FB\\DEMOWOLVOX\\2025\\WOLVOX.FDB',
                user: 'SYSDBA',
                password: 'masterkey'
            },
            wolvoxStatus: null,
            wolvoxMessage: ''
        }
    },
    methods: {
        async testWolvox() {
            try {
                const response = await fetch('/api/test/wolvox', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.wolvox)
                })
                const data = await response.json()
                this.wolvoxStatus = data.success
                this.wolvoxMessage = data.message
            } catch (error) {
                this.wolvoxStatus = false
                this.wolvoxMessage = error.message
            }
        }
    }
} 