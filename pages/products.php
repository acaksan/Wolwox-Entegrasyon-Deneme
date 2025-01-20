<?php
// Wolvox'tan ürünleri çek
function getWolvoxProducts($pdo, $page = 1, $limit = 10) {
    $offset = ($page - 1) * $limit;
    $query = "SELECT FIRST $limit SKIP $offset 
              STK_KODU, STK_ADI, SATIS_FIYATI1, BAKIYE 
              FROM STOKLAR 
              WHERE AKTIF = 1";
    
    try {
        $stmt = $pdo->query($query);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch (PDOException $e) {
        displayMessage('Ürünler çekilirken hata oluştu: ' . $e->getMessage(), 'error');
        return [];
    }
}

// WooCommerce'dan ürünleri çek
function getWooProducts($woocommerce, $page = 1, $limit = 10) {
    try {
        return $woocommerce->get('products', [
            'page' => $page,
            'per_page' => $limit
        ]);
    } catch (Exception $e) {
        displayMessage('WooCommerce ürünleri çekilirken hata oluştu: ' . $e->getMessage(), 'error');
        return [];
    }
}

// Sayfalama parametreleri
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 10;

// Bağlantıları kontrol et
$wolvoxProducts = [];
$wooProducts = [];

if (isset($_SESSION['settings'])) {
    // Wolvox bağlantısı
    try {
        $dsn = "firebird:dbname={$_SESSION['settings']['wolvox']['host']}:{$_SESSION['settings']['wolvox']['database']};charset=UTF8";
        $pdo = new PDO($dsn, $_SESSION['settings']['wolvox']['username'], $_SESSION['settings']['wolvox']['password']);
        $wolvoxProducts = getWolvoxProducts($pdo, $page, $limit);
    } catch (PDOException $e) {
        displayMessage('Wolvox bağlantı hatası: ' . $e->getMessage(), 'error');
    }

    // WooCommerce bağlantısı
    try {
        $woocommerce = new Automattic\WooCommerce\Client(
            $_SESSION['settings']['woocommerce']['url'],
            $_SESSION['settings']['woocommerce']['consumer_key'],
            $_SESSION['settings']['woocommerce']['consumer_secret'],
            ['version' => 'wc/v3']
        );
        $wooProducts = getWooProducts($woocommerce, $page, $limit);
    } catch (Exception $e) {
        displayMessage('WooCommerce bağlantı hatası: ' . $e->getMessage(), 'error');
    }
}
?>

<div class="row mb-4">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <button class="btn btn-primary me-2" data-bs-toggle="modal" data-bs-target="#syncModal">
                    <i class="fas fa-sync"></i> Senkronize Et
                </button>
                <button class="btn btn-success">
                    <i class="fas fa-plus"></i> Yeni Ürün
                </button>
            </div>
            <div class="d-flex gap-2">
                <input type="text" class="form-control" placeholder="Ürün Ara...">
                <button class="btn btn-outline-primary">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- Wolvox Ürünleri -->
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Wolvox Ürünleri</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Stok Kodu</th>
                                <th>Ürün Adı</th>
                                <th>Fiyat</th>
                                <th>Stok</th>
                                <th>İşlem</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($wolvoxProducts)): ?>
                                <tr>
                                    <td colspan="5" class="text-center">Ürün bulunamadı veya bağlantı hatası.</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($wolvoxProducts as $product): ?>
                                    <tr>
                                        <td><?php echo htmlspecialchars($product['STK_KODU']); ?></td>
                                        <td><?php echo htmlspecialchars($product['STK_ADI']); ?></td>
                                        <td><?php echo number_format($product['SATIS_FIYATI1'], 2); ?> ₺</td>
                                        <td><?php echo number_format($product['BAKIYE'], 0); ?></td>
                                        <td>
                                            <button class="btn btn-sm btn-info" title="WooCommerce'a Aktar">
                                                <i class="fas fa-arrow-right"></i>
                                            </button>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- WooCommerce Ürünleri -->
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">WooCommerce Ürünleri</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Ürün Adı</th>
                                <th>Fiyat</th>
                                <th>Stok</th>
                                <th>İşlem</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($wooProducts)): ?>
                                <tr>
                                    <td colspan="5" class="text-center">Ürün bulunamadı veya bağlantı hatası.</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($wooProducts as $product): ?>
                                    <tr>
                                        <td><?php echo $product->id; ?></td>
                                        <td><?php echo htmlspecialchars($product->name); ?></td>
                                        <td><?php echo number_format($product->price, 2); ?> ₺</td>
                                        <td><?php echo $product->stock_quantity ?? 'N/A'; ?></td>
                                        <td>
                                            <button class="btn btn-sm btn-primary" title="Düzenle">
                                                <i class="fas fa-edit"></i>
                                            </button>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Senkronizasyon Modal -->
<div class="modal fade" id="syncModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Ürün Senkronizasyonu</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label class="form-label">Senkronizasyon Yönü</label>
                    <select class="form-select">
                        <option value="wolvox_to_woo">Wolvox → WooCommerce</option>
                        <option value="woo_to_wolvox">WooCommerce → Wolvox</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Senkronize Edilecek Veriler</label>
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="sync_names" checked>
                        <label class="form-check-label" for="sync_names">Ürün Adları</label>
                    </div>
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="sync_prices" checked>
                        <label class="form-check-label" for="sync_prices">Fiyatlar</label>
                    </div>
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="sync_stock" checked>
                        <label class="form-check-label" for="sync_stock">Stok Miktarları</label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">İptal</button>
                <button type="button" class="btn btn-primary">Senkronize Et</button>
            </div>
        </div>
    </div>
</div>
