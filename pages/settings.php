<?php
$security = Security::getInstance();
$message = null;

// WooCommerce bağlantı testi
if (isset($_POST['test_woo'])) {
    try {
        require_once 'vendor/autoload.php';
        
        $woocommerce = new Automattic\WooCommerce\Client(
            $_POST['woo_url'],
            $_POST['woo_key'],
            $_POST['woo_secret'],
            [
                'wp_api' => true,
                'version' => 'wc/v3',
                'verify_ssl' => false
            ]
        );
        
        // Test için ürünleri çekmeyi dene
        $products = $woocommerce->get('products', ['per_page' => 1]);
        
        $message = [
            'type' => 'success',
            'text' => 'WooCommerce bağlantısı başarılı!'
        ];
    } catch (Exception $e) {
        $message = [
            'type' => 'error',
            'text' => 'WooCommerce bağlantı hatası: ' . $e->getMessage()
        ];
    }
}

// Wolvox bağlantı testi
if (isset($_POST['test_wolvox'])) {
    try {
        if (!extension_loaded('interbase')) {
            throw new Exception('Firebird eklentisi yüklü değil. Lütfen php_interbase.dll dosyasını PHP kurulumunuza ekleyin.');
        }
        
        $host = $_POST['wolvox_host'];
        $database = $_POST['wolvox_database'];
        $username = $_POST['wolvox_user'];
        $password = $_POST['wolvox_password'];
        
        $dsn = $host . ':' . $database;
        
        $db = ibase_connect($dsn, $username, $password, 'UTF8');
        
        if ($db === false) {
            throw new Exception(ibase_errmsg());
        }
        
        // Test sorgusu
        $query = "SELECT FIRST 1 * FROM RDB\$DATABASE";
        $result = ibase_query($db, $query);
        
        if ($result === false) {
            throw new Exception(ibase_errmsg());
        }
        
        ibase_free_result($result);
        ibase_close($db);
        
        $message = [
            'type' => 'success',
            'text' => 'Wolvox bağlantısı başarılı!'
        ];
    } catch (Exception $e) {
        $message = [
            'type' => 'error',
            'text' => 'Wolvox bağlantı hatası: ' . $e->getMessage()
        ];
    }
}

// Ayarları kaydet
if (isset($_POST['save_settings'])) {
    try {
        // Ayarları kaydet
        // TODO: Ayarları veritabanına kaydet
        
        $message = [
            'type' => 'success',
            'text' => 'Ayarlar başarıyla kaydedildi!'
        ];
    } catch (Exception $e) {
        $message = [
            'type' => 'error',
            'text' => 'Ayarlar kaydedilirken hata oluştu: ' . $e->getMessage()
        ];
    }
}

// Mesaj varsa göster
if ($message) {
    echo '<div class="alert alert-' . ($message['type'] === 'success' ? 'success' : 'danger') . ' alert-dismissible fade show" role="alert">
            ' . htmlspecialchars($message['text']) . '
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>';
}
?>

<div class="container-fluid">
    <div class="row">
        <div class="col-md-6">
            <!-- WooCommerce Ayarları -->
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0 fw-bold">WooCommerce Ayarları</h5>
                </div>
                <div class="card-body">
                    <form method="post" action="">
                        <?php echo $security->generateFormToken(); ?>
                        
                        <div class="mb-3">
                            <label class="form-label">Site URL</label>
                            <input type="url" name="woo_url" class="form-control" value="<?php echo WC_URL; ?>" required>
                            <div class="form-text">Örnek: https://www.siteniz.com</div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Consumer Key</label>
                            <input type="text" name="woo_key" class="form-control" value="<?php echo WC_CONSUMER_KEY; ?>" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Consumer Secret</label>
                            <input type="text" name="woo_secret" class="form-control" value="<?php echo WC_CONSUMER_SECRET; ?>" required>
                        </div>
                        
                        <button type="submit" name="test_woo" class="btn btn-primary">
                            <i class="fas fa-plug me-2"></i>Bağlantıyı Test Et
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <!-- Wolvox Ayarları -->
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0 fw-bold">Wolvox Ayarları</h5>
                </div>
                <div class="card-body">
                    <form method="post" action="">
                        <?php echo $security->generateFormToken(); ?>
                        
                        <div class="mb-3">
                            <label class="form-label">Sunucu</label>
                            <input type="text" name="wolvox_host" class="form-control" value="<?php echo FB_HOST; ?>" required>
                            <div class="form-text">Örnek: localhost</div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Veritabanı Yolu</label>
                            <input type="text" name="wolvox_database" class="form-control" value="<?php echo FB_DATABASE; ?>" required>
                            <div class="form-text">Örnek: C:\WOLVOX8\Database\WOLVOX.FDB</div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Kullanıcı Adı</label>
                            <input type="text" name="wolvox_user" class="form-control" value="<?php echo FB_USERNAME; ?>" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Şifre</label>
                            <input type="password" name="wolvox_password" class="form-control" value="<?php echo FB_PASSWORD; ?>" required>
                        </div>
                        
                        <button type="submit" name="test_wolvox" class="btn btn-primary">
                            <i class="fas fa-database me-2"></i>Bağlantıyı Test Et
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Kaydet Butonu -->
    <div class="row">
        <div class="col-12">
            <form method="post" action="" class="text-end">
                <?php echo $security->generateFormToken(); ?>
                <button type="submit" name="save_settings" class="btn btn-success">
                    <i class="fas fa-save me-2"></i>Ayarları Kaydet
                </button>
            </form>
        </div>
    </div>
</div>
