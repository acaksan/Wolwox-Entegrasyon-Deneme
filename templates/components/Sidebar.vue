<template>
  <nav class="fixed top-0 left-0 h-full w-64 bg-white shadow-lg">
    <div class="p-4 border-b">
      <h1 class="text-xl font-bold text-gray-800">Lastik Entegrasyon</h1>
      <p class="text-sm text-gray-500">Wolvox - WooCommerce</p>
    </div>
    
    <div class="overflow-y-auto h-full pb-20">
      <div v-for="group in activeMenuGroups" 
           :key="group.id" 
           class="border-t">
        <div class="p-4 text-sm text-gray-500">{{ group.title }}</div>
        <template v-for="item in activeItems(group)" :key="item.id">
          <a :href="item.path" 
             class="block p-4 hover:bg-gray-100">
            <i :class="item.icon + ' w-6'"></i>
            {{ item.name }}
            <span v-if="item.status === 'development'"
                  class="float-right text-xs bg-yellow-500 text-white px-2 py-1 rounded">
              Yapım Aşamasında
            </span>
          </a>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { menuStructure } from '@/config/menu-structure'

export default {
  setup() {
    const activeMenuGroups = computed(() => 
      menuStructure.items.filter(group => group.active)
    )

    const activeItems = (group) => 
      group.items.filter(item => item.active)

    return {
      activeMenuGroups,
      activeItems
    }
  }
}
</script> 