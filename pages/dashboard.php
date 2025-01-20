<?php
// Örnek veriler (daha sonra gerçek verilerle değiştirilecek)
$stats = [
    'orders' => [
        'title' => 'SİPARİŞLER',
        'value' => '0',
        'icon' => 'fas fa-shopping-cart',
        'color' => 'primary'
    ],
    'revenue' => [
        'title' => 'GELİR',
        'value' => '0 ₺',
        'icon' => 'fas fa-lira-sign',
        'color' => 'success'
    ],
    'products' => [
        'title' => 'ÜRÜNLER',
        'value' => '0',
        'icon' => 'fas fa-box',
        'color' => 'info'
    ],
    'customers' => [
        'title' => 'MÜŞTERİLER',
        'value' => '0',
        'icon' => 'fas fa-users',
        'color' => 'warning'
    ]
];

$syncStatus = [
    ['title' => 'Son Ürün Senkronizasyonu', 'time' => '-'],
    ['title' => 'Son Sipariş Senkronizasyonu', 'time' => '-'],
    ['title' => 'Son Stok Senkronizasyonu', 'time' => '-'],
    ['title' => 'Son Fiyat Senkronizasyonu', 'time' => '-']
];

// Stok verilerini çek
try {
    $stocks = getStockData();
} catch (Exception $e) {
    displayMessage($e->getMessage(), 'error');
    $stocks = [];
}
?>

<div class="container-fluid">
    <!-- Üst butonlar -->
    <div class="d-flex justify-content-end mb-4">
        <button class="btn btn-primary me-2" id="syncButton">
            <i class="fas fa-sync-alt me-2"></i> Senkronize Et
        </button>
        <button class="btn btn-success">
            <i class="fas fa-plus me-2"></i> Yeni Ürün
        </button>
    </div>

    <!-- İstatistik kartları -->
    <div class="row mb-4">
        <?php foreach ($stats as $key => $stat): ?>
        <div class="col-md-3 mb-4">
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="rounded-circle p-3 bg-<?php echo $stat['color']; ?> bg-opacity-10 me-3">
                            <i class="<?php echo $stat['icon']; ?> text-<?php echo $stat['color']; ?> fa-lg"></i>
                        </div>
                        <div>
                            <h6 class="text-muted mb-1 text-uppercase small">
                                <?php echo $stat['title']; ?>
                            </h6>
                            <h3 class="mb-0 fw-bold">
                                <?php echo $stat['value']; ?>
                            </h3>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
    </div>

    <!-- Ana içerik -->
    <div class="row">
        <!-- Son Siparişler -->
        <div class="col-md-8 mb-4">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0 fw-bold">Son Siparişler</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Sipariş No</th>
                                    <th>Müşteri</th>
                                    <th>Tutar</th>
                                    <th>Durum</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td colspan="4" class="text-center text-muted py-4">
                                        Henüz sipariş bulunmuyor
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Senkronizasyon Durumu -->
        <div class="col-md-4 mb-4">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0 fw-bold">Senkronizasyon Durumu</h5>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <?php foreach ($syncStatus as $status): ?>
                        <div class="list-group-item px-0 py-3 d-flex justify-content-between align-items-center border-bottom">
                            <div class="me-auto">
                                <h6 class="mb-0"><?php echo $status['title']; ?></h6>
                            </div>
                            <span class="text-muted"><?php echo $status['time']; ?></span>
                        </div>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Stok Listesi -->
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Stok Listesi</h5>
            <div>
                <button type="button" class="btn btn-primary btn-sm" onclick="syncStocks()">
                    <i class="fas fa-sync-alt me-1"></i> Senkronize Et
                </button>
                <button type="button" class="btn btn-secondary btn-sm">
                    <i class="fas fa-filter me-1"></i> Filtrele
                </button>
            </div>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>STOK KODU</th>
                            <th>STOK ADI</th>
                            <th>BİRİM</th>
                            <th>SATIŞ FİYATI</th>
                            <th>KDV ORANI</th>
                            <th>STOK MİKTARI</th>
                            <th>İŞLEMLER</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php if (empty($stocks)): ?>
                        <tr>
                            <td colspan="7" class="text-center py-4">
                                <i class="fas fa-box text-muted mb-2 fa-2x"></i>
                                <p class="text-muted mb-0">Henüz stok bulunmuyor</p>
                            </td>
                        </tr>
                        <?php else: ?>
                            <?php foreach ($stocks as $stock): ?>
                            <tr>
                                <td><?php echo htmlspecialchars($stock['stok_kodu']); ?></td>
                                <td><?php echo htmlspecialchars($stock['stok_adi']); ?></td>
                                <td><?php echo htmlspecialchars($stock['birim']); ?></td>
                                <td><?php echo formatPrice($stock['satis_fiyati']); ?></td>
                                <td>%<?php echo number_format($stock['kdv_orani'], 0); ?></td>
                                <td><?php echo number_format($stock['stok_miktari'], 2); ?></td>
                                <td>
                                    <button type="button" class="btn btn-primary btn-sm" title="Senkronize Et" onclick="syncStock('<?php echo htmlspecialchars($stock['stok_kodu']); ?>')">
                                        <i class="fas fa-sync-alt"></i>
                                    </button>
                                    <button type="button" class="btn btn-success btn-sm" title="Düzenle" onclick="editStock('<?php echo htmlspecialchars($stock['stok_kodu']); ?>')">
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

<!-- Senkronizasyon Modal -->
<div class="modal fade" id="syncModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Stok Senkronizasyonu</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Stok verileri WooCommerce ile senkronize ediliyor...</p>
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 0%"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Senkronizasyon butonu tıklama olayı
$('#syncButton').click(function() {
    var button = $(this);
    button.prop('disabled', true);
    button.html('<i class="fas fa-spinner fa-spin me-2"></i> Senkronize Ediliyor...');
    
    // 3 saniye sonra butonu eski haline getir (test amaçlı)
    setTimeout(function() {
        button.prop('disabled', false);
        button.html('<i class="fas fa-sync-alt me-2"></i> Senkronize Et');
    }, 3000);
});

function syncStocks() {
    if (confirm('Tüm stokları WooCommerce ile senkronize etmek istediğinize emin misiniz?')) {
        // Modal'ı göster
        var syncModal = new bootstrap.Modal(document.getElementById('syncModal'));
        syncModal.show();
        
        // AJAX isteği
        fetch('ajax/sync_stocks.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Başarılı
                location.reload();
            } else {
                // Hata
                alert('Senkronizasyon sırasında bir hata oluştu: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Senkronizasyon sırasında bir hata oluştu');
        })
        .finally(() => {
            syncModal.hide();
        });
    }
}

function syncStock(stockCode) {
    if (confirm('Bu stoku WooCommerce ile senkronize etmek istediğinize emin misiniz?')) {
        // AJAX isteği
        fetch('ajax/sync_stock.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                stock_code: stockCode
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Stok başarıyla senkronize edildi');
                location.reload();
            } else {
                alert('Senkronizasyon sırasında bir hata oluştu: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Senkronizasyon sırasında bir hata oluştu');
        });
    }
}

function editStock(stockCode) {
    window.location.href = 'index.php?page=edit_stock&code=' + encodeURIComponent(stockCode);
}
</script>
