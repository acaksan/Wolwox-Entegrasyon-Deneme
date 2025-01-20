<?php
// Dashboard için örnek veriler
$stats = [
    'orders' => ['count' => 150, 'trend' => '+12%', 'icon' => 'shopping-cart', 'color' => 'primary'],
    'revenue' => ['count' => '₺25,430', 'trend' => '+8%', 'icon' => 'dollar-sign', 'color' => 'success'],
    'products' => ['count' => 1250, 'trend' => '+5%', 'icon' => 'box', 'color' => 'info'],
    'customers' => ['count' => 450, 'trend' => '+15%', 'icon' => 'users', 'color' => 'warning']
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

    <!-- Stats Cards -->
    <div class="row">
        <?php foreach ($stats as $key => $stat): ?>
            <div class="col-md-3 mb-4">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="text-muted text-uppercase"><?php echo ucfirst($key); ?></h6>
                                <h3 class="mb-0"><?php echo $stat['count']; ?></h3>
                            </div>
                            <div class="rounded-circle p-3 bg-<?php echo $stat['color']; ?> bg-opacity-10">
                                <i class="fas fa-<?php echo $stat['icon']; ?> text-<?php echo $stat['color']; ?> fa-2x"></i>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span class="text-success">
                                <i class="fas fa-arrow-up"></i> <?php echo $stat['trend']; ?>
                            </span>
                            <span class="text-muted">son 30 günde</span>
                        </div>
                    </div>
                </div>
            </div>
        <?php endforeach; ?>
    </div>

    <div class="row">
        <!-- Recent Orders -->
        <div class="col-md-8 mb-4">
            <div class="card">
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
                                    <th>Durum</th>
                                    <th>Tutar</th>
                                    <th>Tarih</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>#1234</td>
                                    <td>Ahmet Yılmaz</td>
                                    <td><span class="badge bg-success">Tamamlandı</span></td>
                                    <td>₺1,250</td>
                                    <td>20.01.2025</td>
                                </tr>
                                <tr>
                                    <td>#1233</td>
                                    <td>Mehmet Demir</td>
                                    <td><span class="badge bg-warning">Hazırlanıyor</span></td>
                                    <td>₺850</td>
                                    <td>20.01.2025</td>
                                </tr>
                                <tr>
                                    <td>#1232</td>
                                    <td>Ayşe Kaya</td>
                                    <td><span class="badge bg-info">Kargoda</span></td>
                                    <td>₺2,150</td>
                                    <td>19.01.2025</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Stock Alerts -->
        <div class="col-md-4 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Stok Uyarıları</h5>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Ürün A</h6>
                                    <small class="text-danger">Kritik stok seviyesi</small>
                                </div>
                                <span class="badge bg-danger">2 adet</span>
                            </div>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Ürün B</h6>
                                    <small class="text-warning">Düşük stok</small>
                                </div>
                                <span class="badge bg-warning">5 adet</span>
                            </div>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="mb-1">Ürün C</h6>
                                    <small class="text-warning">Düşük stok</small>
                                </div>
                                <span class="badge bg-warning">8 adet</span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
