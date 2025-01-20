<?php
// Ayarları kaydet
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['save_settings'])) {
        // WooCommerce ayarlarını kaydet
        $woocommerce = [
            'url' => $_POST['woo_url'] ?? '',
            'consumer_key' => $_POST['woo_consumer_key'] ?? '',
            'consumer_secret' => $_POST['woo_consumer_secret'] ?? ''
        ];
        
        // Wolvox ayarlarını kaydet
        $wolvox = [
            'server' => $_POST['wolvox_server'] ?? '',
            'database' => $_POST['wolvox_database'] ?? '',
            'username' => $_POST['wolvox_username'] ?? '',
            'password' => $_POST['wolvox_password'] ?? ''
        ];
        
        // Ayarları kaydet (örnek olarak session'da tutuyoruz)
        $_SESSION['settings'] = [
            'woocommerce' => $woocommerce,
            'wolvox' => $wolvox
        ];
        
        displayMessage('Ayarlar başarıyla kaydedildi.', 'success');
    }
}

// Kaydedilmiş ayarları al
$settings = $_SESSION['settings'] ?? [
    'woocommerce' => [
        'url' => '',
        'consumer_key' => '',
        'consumer_secret' => ''
    ],
    'wolvox' => [
        'server' => '',
        'database' => '',
        'username' => '',
        'password' => ''
    ]
];
?>

<div class="row">
    <div class="col-12">
        <form method="post" id="settingsForm">
            <!-- WooCommerce Ayarları -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fab fa-wordpress me-2"></i>
                        WooCommerce Bağlantı Ayarları
                    </h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="woo_url" class="form-label">Web Sitesi URL</label>
                        <input type="url" class="form-control" id="woo_url" name="woo_url" 
                               value="<?php echo htmlspecialchars($settings['woocommerce']['url']); ?>" 
                               placeholder="https://example.com">
                        <div class="form-text">WooCommerce sitenizin tam URL'sini girin</div>
                    </div>
                    <div class="mb-3">
                        <label for="woo_consumer_key" class="form-label">Consumer Key</label>
                        <input type="text" class="form-control" id="woo_consumer_key" name="woo_consumer_key" 
                               value="<?php echo htmlspecialchars($settings['woocommerce']['consumer_key']); ?>">
                    </div>
                    <div class="mb-3">
                        <label for="woo_consumer_secret" class="form-label">Consumer Secret</label>
                        <input type="password" class="form-control" id="woo_consumer_secret" name="woo_consumer_secret" 
                               value="<?php echo htmlspecialchars($settings['woocommerce']['consumer_secret']); ?>">
                    </div>
                    <button type="button" class="btn btn-info" onclick="testWooConnection()">
                        <i class="fas fa-plug me-2"></i>
                        Bağlantıyı Test Et
                    </button>
                </div>
            </div>

            <!-- Wolvox Ayarları -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-database me-2"></i>
                        Wolvox Bağlantı Ayarları
                    </h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label for="wolvox_server" class="form-label">Sunucu</label>
                        <input type="text" class="form-control" id="wolvox_server" name="wolvox_server" 
                               value="<?php echo htmlspecialchars($settings['wolvox']['server']); ?>" 
                               placeholder="localhost">
                    </div>
                    <div class="mb-3">
                        <label for="wolvox_database" class="form-label">Veritabanı</label>
                        <input type="text" class="form-control" id="wolvox_database" name="wolvox_database" 
                               value="<?php echo htmlspecialchars($settings['wolvox']['database']); ?>">
                    </div>
                    <div class="mb-3">
                        <label for="wolvox_username" class="form-label">Kullanıcı Adı</label>
                        <input type="text" class="form-control" id="wolvox_username" name="wolvox_username" 
                               value="<?php echo htmlspecialchars($settings['wolvox']['username']); ?>">
                    </div>
                    <div class="mb-3">
                        <label for="wolvox_password" class="form-label">Şifre</label>
                        <input type="password" class="form-control" id="wolvox_password" name="wolvox_password" 
                               value="<?php echo htmlspecialchars($settings['wolvox']['password']); ?>">
                    </div>
                    <button type="button" class="btn btn-info" onclick="testWolvoxConnection()">
                        <i class="fas fa-plug me-2"></i>
                        Bağlantıyı Test Et
                    </button>
                </div>
            </div>

            <!-- Kaydet Butonu -->
            <div class="text-end">
                <button type="submit" name="save_settings" class="btn btn-primary">
                    <i class="fas fa-save me-2"></i>
                    Ayarları Kaydet
                </button>
            </div>
        </form>
    </div>
</div>

<script>
// WooCommerce bağlantı testi
async function testWooConnection() {
    const url = document.getElementById('woo_url').value;
    const consumer_key = document.getElementById('woo_consumer_key').value;
    const consumer_secret = document.getElementById('woo_consumer_secret').value;
    
    if (!url || !consumer_key || !consumer_secret) {
        alert('Lütfen tüm WooCommerce bağlantı bilgilerini doldurun.');
        return;
    }
    
    try {
        // AJAX isteği gönder
        const response = await fetch('ajax/test_woo_connection.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url,
                consumer_key,
                consumer_secret
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('WooCommerce bağlantısı başarılı!');
        } else {
            alert('WooCommerce bağlantı hatası: ' + data.message);
        }
    } catch (error) {
        alert('Bağlantı testi sırasında bir hata oluştu: ' + error.message);
    }
}

// Wolvox bağlantı testi
async function testWolvoxConnection() {
    const server = document.getElementById('wolvox_server').value;
    const database = document.getElementById('wolvox_database').value;
    const username = document.getElementById('wolvox_username').value;
    const password = document.getElementById('wolvox_password').value;
    
    if (!server || !database || !username || !password) {
        alert('Lütfen tüm Wolvox bağlantı bilgilerini doldurun.');
        return;
    }
    
    try {
        // AJAX isteği gönder
        const response = await fetch('ajax/test_wolvox_connection.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                server,
                database,
                username,
                password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Wolvox bağlantısı başarılı!');
        } else {
            alert('Wolvox bağlantı hatası: ' + data.message);
        }
    } catch (error) {
        alert('Bağlantı testi sırasında bir hata oluştu: ' + error.message);
    }
}
</script>
