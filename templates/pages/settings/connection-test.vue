<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold">Bağlantı Testi</h1>

    <!-- Wolvox Bağlantı Testi -->
    <div class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Wolvox Bağlantısı</h2>
      
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Sunucu</label>
          <input v-model="wolvox.host" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Veritabanı</label>
          <input v-model="wolvox.database" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Kullanıcı</label>
          <input v-model="wolvox.user" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Şifre</label>
          <input v-model="wolvox.password" type="password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
      </div>

      <div class="flex items-center">
        <button @click="testWolvox" 
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Bağlantıyı Test Et
        </button>
        <span v-if="wolvoxStatus" 
              :class="{'text-green-500': wolvoxStatus === 'success', 'text-red-500': wolvoxStatus === 'error'}"
              class="ml-4">
          {{ wolvoxMessage }}
        </span>
      </div>
    </div>

    <!-- WooCommerce Bağlantı Testi -->
    <div class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">WooCommerce Bağlantısı</h2>
      
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Site URL</label>
          <input v-model="woo.url" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Consumer Key</label>
          <input v-model="woo.key" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Consumer Secret</label>
          <input v-model="woo.secret" type="password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
        </div>
      </div>

      <div class="flex items-center">
        <button @click="testWoo" 
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Bağlantıyı Test Et
        </button>
        <span v-if="wooStatus" 
              :class="{'text-green-500': wooStatus === 'success', 'text-red-500': wooStatus === 'error'}"
              class="ml-4">
          {{ wooMessage }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      wolvox: {
        host: '',
        database: '',
        user: '',
        password: ''
      },
      woo: {
        url: '',
        key: '',
        secret: ''
      },
      wolvoxStatus: null,
      wolvoxMessage: '',
      wooStatus: null,
      wooMessage: ''
    }
  },
  async created() {
    // Mevcut ayarları yükle
    await this.loadSettings()
  },
  methods: {
    async loadSettings() {
      try {
        const [wolvoxResponse, wooResponse] = await Promise.all([
          fetch('/api/settings/wolvox'),
          fetch('/api/settings/woocommerce')
        ])
        
        const wolvoxData = await wolvoxResponse.json()
        const wooData = await wooResponse.json()
        
        this.wolvox = wolvoxData
        this.woo = wooData
      } catch (error) {
        console.error('Ayarlar yüklenirken hata:', error)
      }
    },
    async testWolvox() {
      try {
        const response = await fetch('/api/test/wolvox', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.wolvox)
        })
        
        const data = await response.json()
        
        if (data.success) {
          this.wolvoxStatus = 'success'
          this.wolvoxMessage = 'Bağlantı başarılı!'
        } else {
          this.wolvoxStatus = 'error'
          this.wolvoxMessage = `Hata: ${data.message}`
        }
      } catch (error) {
        this.wolvoxStatus = 'error'
        this.wolvoxMessage = `Bağlantı hatası: ${error.message}`
      }
    },
    async testWoo() {
      try {
        const response = await fetch('/api/test/woocommerce', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.woo)
        })
        
        const data = await response.json()
        
        if (data.success) {
          this.wooStatus = 'success'
          this.wooMessage = 'Bağlantı başarılı!'
        } else {
          this.wooStatus = 'error'
          this.wooMessage = `Hata: ${data.message}`
        }
      } catch (error) {
        this.wooStatus = 'error'
        this.wooMessage = `Bağlantı hatası: ${error.message}`
      }
    }
  }
}
</script> 