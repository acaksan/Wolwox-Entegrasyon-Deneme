<template>
    <div class="space-y-6">
        <h1 class="text-2xl font-bold">Menü Yönetimi</h1>
        
        <div class="bg-white p-6 rounded-lg shadow">
            <div v-for="group in menuConfig" :key="group.id" class="mb-8">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-xl font-semibold">{{ group.title }}</h2>
                    <div class="flex items-center">
                        <label class="switch">
                            <input type="checkbox" v-model="group.active" @change="saveMenuConfig">
                            <span class="slider round"></span>
                        </label>
                    </div>
                </div>
                
                <div class="ml-6 space-y-3">
                    <div v-for="item in group.items" 
                         :key="item.id" 
                         class="flex items-center justify-between p-3 bg-gray-50 rounded">
                        <div class="flex items-center">
                            <i :class="item.icon" class="w-6"></i>
                            <span class="ml-2">{{ item.name }}</span>
                            <span v-if="item.status === 'development'"
                                  class="ml-2 text-xs bg-yellow-500 text-white px-2 py-1 rounded">
                                Yapım Aşamasında
                            </span>
                        </div>
                        <div class="flex items-center space-x-4">
                            <label class="switch">
                                <input type="checkbox" v-model="item.active" @change="saveMenuConfig">
                                <span class="slider round"></span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { menuStructure } from '@/config/menu-structure'

export default {
    setup() {
        const menuConfig = ref(menuStructure)

        const saveMenuConfig = async () => {
            try {
                await fetch('/api/settings/menu', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(menuConfig.value)
                })
                // Başarılı mesajı göster
            } catch (error) {
                console.error('Menü kaydedilirken hata:', error)
            }
        }

        const loadMenuConfig = async () => {
            try {
                const response = await fetch('/api/settings/menu')
                const data = await response.json()
                menuConfig.value = data
            } catch (error) {
                console.error('Menü yüklenirken hata:', error)
            }
        }

        onMounted(loadMenuConfig)

        return {
            menuConfig,
            saveMenuConfig
        }
    }
}
</script>

<style scoped>
.switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:checked + .slider:before {
    transform: translateX(26px);
}

.slider.round {
    border-radius: 34px;
}

.slider.round:before {
    border-radius: 50%;
}
</style> 