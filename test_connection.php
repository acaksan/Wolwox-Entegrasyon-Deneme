<?php
require_once 'config/config.php';

try {
    echo "Yüklü PDO sürücüleri:\n";
    print_r(PDO::getAvailableDrivers());
    echo "\n\n";

    echo "Bağlantı bilgileri:\n";
    echo "Host: " . FB_HOST . "\n";
    echo "Database: " . FB_DATABASE . "\n";
    echo "Username: " . FB_USERNAME . "\n";
    echo "Password: " . FB_PASSWORD . "\n\n";

    $dsn = "firebird:dbname=" . FB_HOST . ":" . FB_DATABASE;
    echo "DSN: " . $dsn . "\n\n";
    
    $pdo = new PDO($dsn, FB_USERNAME, FB_PASSWORD);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Veritabanı bağlantısı başarılı!\n\n";
    
    // Tablo yapısını al
    $query = "SELECT RDB\$FIELD_NAME 
        FROM RDB\$RELATION_FIELDS 
        WHERE RDB\$RELATION_NAME = 'STOK' 
        ORDER BY RDB\$FIELD_POSITION";
    
    $stmt = $pdo->query($query);
    echo "STOK tablosunun alanları:\n";
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        foreach ($row as $key => $value) {
            echo trim($value) . "\n";
        }
    }
    
} catch(PDOException $e) {
    echo "Bağlantı hatası: " . $e->getMessage() . "\n\n";
    echo "Hata kodu: " . $e->getCode() . "\n";
    echo "Hata dosyası: " . $e->getFile() . "\n";
    echo "Hata satırı: " . $e->getLine() . "\n";
} catch(Exception $e) {
    echo "Genel hata: " . $e->getMessage() . "\n\n";
    echo "Hata kodu: " . $e->getCode() . "\n";
    echo "Hata dosyası: " . $e->getFile() . "\n";
    echo "Hata satırı: " . $e->getLine() . "\n";
}
