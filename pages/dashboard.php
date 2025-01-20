<?php
// Örnek veriler (daha sonra gerçek verilerle değiştirilecek)
$stats = [
    'orders' => [
        'title' => 'Siparişler',
        'value' => '0',
        'icon' => 'fas fa-shopping-cart',
        'color' => 'primary'
    ],
    'revenue' => [
        'title' => 'Gelir',
        'value' => '0 ₺',
        'icon' => 'fas fa-lira-sign',
        'color' => 'success'
    ],
    'products' => [
        'title' => 'Ürünler',
        'value' => '0',
        'icon' => 'fas fa-box',
        'color' => 'info'
    ],
    'customers' => [
        'title' => 'Müşteriler',
        'value' => '0',
        'icon' => 'fas fa-users',
        'color' => 'warning'
    ]
];
?>

<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h3">Dashboard</h1>
        <div class="btn-group">
            <button type="button" class="btn btn-primary">
                <i class="fas fa-sync-alt"></i> Senkronize Et
            </button>
            <button type="button" class="btn btn-success">
                <i class="fas fa-plus"></i> Yeni Ürün
            </button>
        </div>
    </div>

    <div class="row">
        <?php foreach ($stats as $key => $stat): ?>
            <div class="col-md-3 mb-4">
                <div class="card border-<?php echo $stat['color']; ?> h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="text-muted text-uppercase font-weight-bold small">
                                    <?php echo $stat['title']; ?>
                                </div>
                                <div class="h3 mb-0">
                                    <?php echo $stat['value']; ?>
                                </div>
                            </div>
                            <div class="h1 text-<?php echo $stat['color']; ?>">
                                <i class="<?php echo $stat['icon']; ?>"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>

    <div class="row">
        <!-- Son Siparişler -->
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="card-title mb-0">Son Siparişler</h5>
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
                                    <td colspan="4" class="text-center">Henüz sipariş bulunmuyor.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Senkronizasyon Durumu -->
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="card-title mb-0">Senkronizasyon Durumu</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table">
                            <tbody>
                                <tr>
                                    <td>Son Ürün Senkronizasyonu</td>
                                    <td class="text-end">-</td>
                                </tr>
                                <tr>
                                    <td>Son Sipariş Senkronizasyonu</td>
                                    <td class="text-end">-</td>
                                </tr>
                                <tr>
                                    <td>Son Stok Senkronizasyonu</td>
                                    <td class="text-end">-</td>
                                </tr>
                                <tr>
                                    <td>Son Fiyat Senkronizasyonu</td>
                                    <td class="text-end">-</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
