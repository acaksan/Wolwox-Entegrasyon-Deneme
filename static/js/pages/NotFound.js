export default {
    name: 'NotFound',
    template: /* html */`
        <div class="text-center py-10">
            <h1 class="text-4xl font-bold text-gray-800 mb-4">404</h1>
            <p class="text-gray-600">Sayfa bulunamadı</p>
            <router-link to="/" 
                        class="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                Ana Sayfaya Dön
            </router-link>
        </div>
    `
} 