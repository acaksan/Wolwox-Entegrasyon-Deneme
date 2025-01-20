<?php
// Sipariş durumları
$orderStatuses = [
    'new' => 'Yeni',
    'pending' => 'Onay Bekliyor',
    'processing' => 'Hazırlanıyor',
    'shipped' => 'Kargoya Verildi',
    'completed' => 'Tamamlandı',
    'cancelled' => 'İptal Edildi'
];

// WooCommerce'dan siparişleri çek
function getWooOrders($woocommerce, $status = 'any', $page = 1, $limit = 10) {
    try {
        return $woocommerce->get('orders', [
            'status' => $status,
            'page' => $page,
            'per_page' => $limit
        ]);
    } catch (Exception $e) {
        displayMessage('WooCommerce siparişleri çekilirken hata oluştu: ' . $e->getMessage(), 'error');
        return [];
    }
}

// Wolvox'a sipariş aktar
function createWolvoxOrder($pdo, $order) {
    try {
        // Sipariş başlığını oluştur
        $query = "INSERT INTO SIPARISLER (TARIH, CARI_KOD, TOPLAM_TUTAR) 
                 VALUES (?, ?, ?) RETURNING SIP_NO";
        $stmt = $pdo->prepare($query);
        $stmt->execute([
            date('Y-m-d'),
            $order->customer_id,
            $order->total
        ]);
        
        $sipNo = $stmt->fetchColumn();
        
        // Sipariş detaylarını oluştur
        foreach ($order->line_items as $item) {
            $query = "INSERT INTO SIPARIS_DETAY (SIP_NO, STK_KODU, MIKTAR, FIYAT) 
                     VALUES (?, ?, ?, ?)";
            $stmt = $pdo->prepare($query);
            $stmt->execute([
                $sipNo,
                $item->sku,
                $item->quantity,
                $item->price
            ]);
        }
        
        return true;
    } catch (PDOException $e) {
        displayMessage('Wolvox sipariş oluşturma hatası: ' . $e->getMessage(), 'error');
        return false;
    }
}

// Filtre ve sayfalama parametreleri
$status = isset($_GET['status']) ? $_GET['status'] : 'any';
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 10;

// Siparişleri çek
$orders = [];
if (isset($_SESSION['settings'])) {
    try {
        $woocommerce = new Automattic\WooCommerce\Client(
            $_SESSION['settings']['woocommerce']['url'],
            $_SESSION['settings']['woocommerce']['consumer_key'],
            $_SESSION['settings']['woocommerce']['consumer_secret'],
            ['version' => 'wc/v3']
        );
        $orders = getWooOrders($woocommerce, $status, $page, $limit);
    } catch (Exception $e) {
        displayMessage('WooCommerce bağlantı hatası: ' . $e->getMessage(), 'error');
    }
}

// Sipariş işlemleri
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['update_status'])) {
        try {
            $woocommerce->put('orders/' . $_POST['order_id'], [
                'status' => $_POST['new_status']
            ]);
            displayMessage('Sipariş durumu güncellendi.', 'success');
        } catch (Exception $e) {
            displayMessage('Sipariş durumu güncellenirken hata oluştu: ' . $e->getMessage(), 'error');
        }
    }
    
    if (isset($_POST['create_wolvox_order'])) {
        try {
            $order = $woocommerce->get('orders/' . $_POST['order_id']);
            
            $dsn = "firebird:dbname={$_SESSION['settings']['wolvox']['host']}:{$_SESSION['settings']['wolvox']['database']};charset=UTF8";
            $pdo = new PDO($dsn, $_SESSION['settings']['wolvox']['username'], $_SESSION['settings']['wolvox']['password']);
            
            if (createWolvoxOrder($pdo, $order)) {
                displayMessage('Sipariş Wolvox\'a aktarıldı.', 'success');
            }
        } catch (Exception $e) {
            displayMessage('Sipariş Wolvox\'a aktarılırken hata oluştu: ' . $e->getMessage(), 'error');
        }
    }
}
?>

<!-- Filtreler -->
<div class="row mb-4">
    <div class="col-md-12">
        <div class="card">
            <div class="card-body">
                <form method="get" class="row g-3">
                    <div class="col-md-3">
                        <label class="form-label">Sipariş Durumu</label>
                        <select name="status" class="form-select">
                            <option value="any">Tümü</option>
                            <?php foreach ($orderStatuses as $key => $value): ?>
                                <option value="<?php echo $key; ?>" <?php echo $status === $key ? 'selected' : ''; ?>>
                                    <?php echo $value; ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Tarih Aralığı</label>
                        <input type="date" class="form-control" name="date_from">
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">&nbsp;</label>
                        <input type="date" class="form-control" name="date_to">
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">&nbsp;</label>
                        <button type="submit" class="btn btn-primary w-100">Filtrele</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Siparişler Tablosu -->
<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title float-start">Siparişler</h5>
                <div class="float-end">
                    <button class="btn btn-success btn-sm" data-bs-toggle="modal" data-bs-target="#bulkActionModal">
                        <i class="fas fa-tasks"></i> Toplu İşlem
                    </button>
                </div>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th><input type="checkbox" class="form-check-input" id="selectAll"></th>
                                <th>Sipariş No</th>
                                <th>Tarih</th>
                                <th>Müşteri</th>
                                <th>Tutar</th>
                                <th>Durum</th>
                                <th>Wolvox</th>
                                <th>İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($orders)): ?>
                                <tr>
                                    <td colspan="8" class="text-center">Sipariş bulunamadı.</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($orders as $order): ?>
                                    <tr>
                                        <td><input type="checkbox" class="form-check-input order-check" value="<?php echo $order->id; ?>"></td>
                                        <td>#<?php echo $order->number; ?></td>
                                        <td><?php echo date('d.m.Y H:i', strtotime($order->date_created)); ?></td>
                                        <td><?php echo $order->billing->first_name . ' ' . $order->billing->last_name; ?></td>
                                        <td><?php echo number_format($order->total, 2); ?> ₺</td>
                                        <td>
                                            <span class="badge bg-<?php echo $order->status === 'completed' ? 'success' : 'warning'; ?>">
                                                <?php echo $orderStatuses[$order->status] ?? $order->status; ?>
                                            </span>
                                        </td>
                                        <td>
                                            <?php if ($order->meta_data && array_search('wolvox_order_id', array_column($order->meta_data, 'key')) !== false): ?>
                                                <span class="badge bg-success">Aktarıldı</span>
                                            <?php else: ?>
                                                <form method="post" class="d-inline">
                                                    <input type="hidden" name="order_id" value="<?php echo $order->id; ?>">
                                                    <button type="submit" name="create_wolvox_order" class="btn btn-sm btn-primary">
                                                        <i class="fas fa-upload"></i> Aktar
                                                    </button>
                                                </form>
                                            <?php endif; ?>
                                        </td>
                                        <td>
                                            <div class="btn-group">
                                                <button type="button" class="btn btn-sm btn-info" title="Görüntüle" 
                                                        data-bs-toggle="modal" data-bs-target="#orderModal" 
                                                        data-order-id="<?php echo $order->id; ?>">
                                                    <i class="fas fa-eye"></i>
                                                </button>
                                                <button type="button" class="btn btn-sm btn-warning" title="Durumu Güncelle"
                                                        data-bs-toggle="modal" data-bs-target="#statusModal"
                                                        data-order-id="<?php echo $order->id; ?>"
                                                        data-order-status="<?php echo $order->status; ?>">
                                                    <i class="fas fa-edit"></i>
                                                </button>
                                            </div>
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

<!-- Sipariş Detay Modal -->
<div class="modal fade" id="orderModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Sipariş Detayı</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6">
                        <h6>Sipariş Bilgileri</h6>
                        <div id="orderDetails"></div>
                    </div>
                    <div class="col-md-6">
                        <h6>Müşteri Bilgileri</h6>
                        <div id="customerDetails"></div>
                    </div>
                </div>
                <hr>
                <h6>Ürünler</h6>
                <div id="orderItems"></div>
            </div>
        </div>
    </div>
</div>

<!-- Durum Güncelleme Modal -->
<div class="modal fade" id="statusModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Sipariş Durumunu Güncelle</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form method="post">
                    <input type="hidden" name="order_id" id="statusOrderId">
                    <div class="mb-3">
                        <label class="form-label">Yeni Durum</label>
                        <select name="new_status" class="form-select">
                            <?php foreach ($orderStatuses as $key => $value): ?>
                                <option value="<?php echo $key; ?>"><?php echo $value; ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <button type="submit" name="update_status" class="btn btn-primary">Güncelle</button>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Toplu İşlem Modal -->
<div class="modal fade" id="bulkActionModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Toplu İşlem</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form method="post">
                    <input type="hidden" name="order_ids" id="bulkOrderIds">
                    <div class="mb-3">
                        <label class="form-label">İşlem</label>
                        <select name="bulk_action" class="form-select">
                            <option value="status">Durum Güncelle</option>
                            <option value="wolvox">Wolvox'a Aktar</option>
                            <option value="invoice">Fatura Oluştur</option>
                        </select>
                    </div>
                    <div class="mb-3" id="bulkStatusSelect">
                        <label class="form-label">Yeni Durum</label>
                        <select name="bulk_status" class="form-select">
                            <?php foreach ($orderStatuses as $key => $value): ?>
                                <option value="<?php echo $key; ?>"><?php echo $value; ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <button type="submit" name="bulk_action_submit" class="btn btn-primary">Uygula</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
// Sipariş detaylarını yükle
document.querySelectorAll('[data-bs-target="#orderModal"]').forEach(button => {
    button.addEventListener('click', function() {
        const orderId = this.dataset.orderId;
        // Ajax ile sipariş detaylarını çek
        // Örnek: fetch(`api/orders/${orderId}`).then(...)
    });
});

// Durum güncelleme modalı
document.querySelectorAll('[data-bs-target="#statusModal"]').forEach(button => {
    button.addEventListener('click', function() {
        const orderId = this.dataset.orderId;
        const status = this.dataset.orderStatus;
        document.getElementById('statusOrderId').value = orderId;
        document.querySelector('#statusModal select').value = status;
    });
});

// Toplu seçim
document.getElementById('selectAll').addEventListener('change', function() {
    document.querySelectorAll('.order-check').forEach(checkbox => {
        checkbox.checked = this.checked;
    });
});

// Toplu işlem modalı
document.querySelector('#bulkActionModal form').addEventListener('submit', function(e) {
    const selectedOrders = Array.from(document.querySelectorAll('.order-check:checked')).map(cb => cb.value);
    if (selectedOrders.length === 0) {
        e.preventDefault();
        alert('Lütfen en az bir sipariş seçin.');
    } else {
        document.getElementById('bulkOrderIds').value = selectedOrders.join(',');
    }
});

// Bulk action değiştiğinde status select'i göster/gizle
document.querySelector('select[name="bulk_action"]').addEventListener('change', function() {
    const statusSelect = document.getElementById('bulkStatusSelect');
    statusSelect.style.display = this.value === 'status' ? 'block' : 'none';
});
</script>
