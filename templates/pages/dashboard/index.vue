<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <stat-card
        v-for="stat in stats"
        :key="stat.id"
        :title="stat.title"
        :value="stat.value"
        :icon="stat.icon"
      />
    </div>
  </div>
</template>

<script>
import StatCard from '../../components/StatCard.vue'

export default {
  components: {
    StatCard
  },
  data() {
    return {
      stats: [
        {
          id: 1,
          title: 'Toplam Ürün',
          value: 0,
          icon: 'fas fa-box'
        }
        // ... diğer istatistikler
      ]
    }
  }
}
</script> 