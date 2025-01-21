<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <Sidebar :is-open="sidebarOpen" />
    <Header @toggle-sidebar="toggleSidebar" />
    
    <main class="ml-64 pt-16 p-8">
      <slot></slot>
    </main>
    
    <Footer />
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

export default {
  components: {
    Sidebar,
    Header,
    Footer
  },
  data() {
    return {
      sidebarOpen: true
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    }
  }
}
</script> 