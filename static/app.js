// WooCommerce API ile iletişim için temel fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    console.log('App.js loaded successfully!');

    // Test fonksiyonu
    function testConnection() {
        console.log('Testing connection...');
        fetch('/')
            .then(response => {
                if (response.ok) {
                    console.log('Server connection successful!');
                } else {
                    console.error('Server connection failed!');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Sayfa yüklendiğinde test et
    testConnection();

    // Test butonu varsa event listener ekle
    const testButton = document.getElementById('test-connection');
    if (testButton) {
        testButton.addEventListener('click', testConnection);
    }
});
