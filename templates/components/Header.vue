<template>
  <header class="ml-64 bg-white shadow-sm">
    <div class="flex justify-between items-center p-4">
      <div class="flex items-center">
        <button @click="toggleSidebar" class="text-gray-500 hover:text-gray-700">
          <i class="fas fa-bars"></i>
        </button>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-500">Son Senkronizasyon: {{ lastSync }}</span>
        <sync-button @sync-completed="updateLastSync" />
      </div>
    </div>
  </header>
</template>

<script>
import SyncButton from './SyncButton.vue'

export default {
  components: {
    SyncButton
  },
  data() {
    return {
      lastSync: 'Hiç'
    }
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggle-sidebar')
    },
    updateLastSync() {
      this.lastSync = new Date().toLocaleString()
    }
  }
}
</script> 