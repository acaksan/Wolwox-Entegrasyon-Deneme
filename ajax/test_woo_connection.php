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

$url = $data['url'] ?? '';
$consumer_key = $data['consumer_key'] ?? '';
$consumer_secret = $data['consumer_secret'] ?? '';

if (!$url || !$consumer_key || !$consumer_secret) {
    echo json_encode([
        'success' => false,
        'message' => 'Eksik parametreler'
    ]);
    exit;
}

// WooCommerce REST API endpoint
$endpoint = rtrim($url, '/') . '/wp-json/wc/v3/system_status';

// Basic auth için kimlik bilgilerini hazırla
$auth = base64_encode($consumer_key . ':' . $consumer_secret);

// cURL isteği oluştur
$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => $endpoint,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => [
        'Authorization: Basic ' . $auth,
        'Content-Type: application/json'
    ],
    CURLOPT_SSL_VERIFYPEER => false // SSL sertifika doğrulamasını devre dışı bırak (geliştirme için)
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
curl_close($ch);

if ($error) {
    echo json_encode([
        'success' => false,
        'message' => 'cURL hatası: ' . $error
    ]);
    exit;
}

if ($httpCode === 200) {
    echo json_encode([
        'success' => true,
        'message' => 'WooCommerce bağlantısı başarılı'
    ]);
} else {
    echo json_encode([
        'success' => false,
        'message' => 'WooCommerce bağlantı hatası. HTTP Kodu: ' . $httpCode
    ]);
}
?>
