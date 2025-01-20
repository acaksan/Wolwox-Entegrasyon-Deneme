<?php
session_start();
header('Content-Type: application/json');

function testWolvoxConnection($host, $database, $username, $password) {
    try {
        $dsn = "firebird:dbname={$host}:{$database};charset=UTF8";
        $pdo = new PDO($dsn, $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Test sorgusu
        $stmt = $pdo->query("SELECT FIRST 1 * FROM STOKLAR");
        $stmt->fetch();
        
        return ['success' => true, 'message' => 'Wolvox bağlantısı başarılı!'];
    } catch (PDOException $e) {
        return ['success' => false, 'message' => 'Wolvox bağlantı hatası: ' . $e->getMessage()];
    }
}

function testWooConnection($url, $consumer_key, $consumer_secret) {
    try {
        require_once __DIR__ . '/../vendor/autoload.php';
        
        $woocommerce = new Automattic\WooCommerce\Client(
            $url,
            $consumer_key,
            $consumer_secret,
            [
                'version' => 'wc/v3',
                'verify_ssl' => false
            ]
        );
        
        // Test için ürünleri çekmeyi dene
        $products = $woocommerce->get('products', ['per_page' => 1]);
        return ['success' => true, 'message' => 'WooCommerce bağlantısı başarılı!'];
    } catch (Exception $e) {
        return ['success' => false, 'message' => 'WooCommerce bağlantı hatası: ' . $e->getMessage()];
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if (!isset($data['type'])) {
        echo json_encode(['success' => false, 'message' => 'Bağlantı tipi belirtilmedi']);
        exit;
    }
    
    if ($data['type'] === 'wolvox') {
        $result = testWolvoxConnection(
            $data['host'] ?? '',
            $data['database'] ?? '',
            $data['username'] ?? '',
            $data['password'] ?? ''
        );
    } elseif ($data['type'] === 'woo') {
        $result = testWooConnection(
            $data['url'] ?? '',
            $data['consumer_key'] ?? '',
            $data['consumer_secret'] ?? ''
        );
    } else {
        $result = ['success' => false, 'message' => 'Geçersiz bağlantı tipi'];
    }
    
    echo json_encode($result);
} else {
    echo json_encode(['success' => false, 'message' => 'Geçersiz istek metodu']);
}
