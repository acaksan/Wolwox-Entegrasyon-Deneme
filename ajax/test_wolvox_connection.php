<?php
header('Content-Type: application/json');

// POST verilerini al
$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    echo json_encode([
        'success' => false,
        'message' => 'Geçersiz istek'
    ]);
    exit;
}

$server = $data['server'] ?? '';
$database = $data['database'] ?? '';
$username = $data['username'] ?? '';
$password = $data['password'] ?? '';

if (!$server || !$database || !$username || !$password) {
    echo json_encode([
        'success' => false,
        'message' => 'Eksik parametreler'
    ]);
    exit;
}

try {
    // PDO bağlantısı oluştur
    $dsn = "sqlsrv:Server=$server;Database=$database";
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ];
    
    $pdo = new PDO($dsn, $username, $password, $options);
    
    // Test sorgusu çalıştır
    $stmt = $pdo->query('SELECT @@VERSION as version');
    $result = $stmt->fetch();
    
    echo json_encode([
        'success' => true,
        'message' => 'Wolvox bağlantısı başarılı. SQL Server versiyonu: ' . $result['version']
    ]);
    
} catch (PDOException $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Veritabanı bağlantı hatası: ' . $e->getMessage()
    ]);
}
?>
