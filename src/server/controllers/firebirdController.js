const firebird = require('../config/firebird');

// Bağlantı ayarlarını kaydet
async function saveConnectionSettings(settings) {
    try {
        // Burada bağlantı ayarlarını .env dosyasına veya veritabanına kaydedebilirsiniz
        // Şimdilik sadece test ediyoruz
        process.env.FB_HOST = settings.host;
        process.env.FB_PORT = settings.port;
        process.env.FB_DATABASE = settings.database;
        process.env.FB_USER = settings.username;
        process.env.FB_PASSWORD = settings.password;
        process.env.FB_CHARSET = settings.charset;

        return { success: true, message: 'Bağlantı ayarları başarıyla kaydedildi.' };
    } catch (error) {
        console.error('Bağlantı ayarları kaydedilirken hata oluştu:', error);
        throw new Error('Bağlantı ayarları kaydedilemedi.');
    }
}

// Bağlantıyı test et
async function testConnection() {
    try {
        const isConnected = await firebird.testConnection();
        if (isConnected) {
            return { success: true, message: 'Bağlantı başarılı.' };
        } else {
            return { success: false, message: 'Bağlantı başarısız.' };
        }
    } catch (error) {
        console.error('Bağlantı testi sırasında hata:', error);
        throw new Error('Bağlantı testi başarısız oldu.');
    }
}

// Ürün detaylarını getir (fiyat ve stok dahil)
async function getProducts() {
    try {
        console.log('Ürün detayları getiriliyor...');
        
        // Önce fiyat ve stok tablolarını kontrol edelim
        const checkTablesSQL = `
            SELECT RDB$RELATION_NAME as TABLE_NAME
            FROM RDB$RELATIONS
            WHERE RDB$SYSTEM_FLAG = 0
            AND RDB$VIEW_BLR IS NULL
            AND (RDB$RELATION_NAME LIKE '%SATIS%FIYAT%' 
                 OR RDB$RELATION_NAME LIKE '%FIYAT%' 
                 OR RDB$RELATION_NAME LIKE '%STOK%FIYAT%'
                 OR RDB$RELATION_NAME LIKE '%DEPO%STOK%'
                 OR RDB$RELATION_NAME LIKE '%STOK%DEPO%')
            ORDER BY RDB$RELATION_NAME
        `;
        
        console.log('Tablo kontrol sorgusu:', checkTablesSQL);
        const tables = await firebird.query(checkTablesSQL);
        console.log('Bulunan tablolar:', tables);
        
        // Şimdilik sadece ürün bilgilerini getirelim
        const sql = `
            SELECT 
                S.*,
                (SELECT FIRST 1 FIYATI FROM STOK_FIYAT WHERE STOKKODU = S.STOKKODU AND TANIMI = 'SATIS FIYATI -1') as SATIS_FIYATI,
                (SELECT SUM(STOK_MIKTARI) FROM STOK_DEPO SD WHERE SD.STOKKODU = S.STOKKODU) as TOPLAM_STOK,
                (SELECT LIST(D.DEPO_ADI || ': ' || SD.STOK_MIKTARI) 
                 FROM STOK_DEPO SD 
                 JOIN DEPOLAR D ON D.DEPO_KODU = SD.DEPOKODU 
                 WHERE SD.STOKKODU = S.STOKKODU) as DEPO_STOKLARI
            FROM STOK S
            WHERE S.STOKKODU = 'PET-100-70-13-175-4000'
        `;
        
        console.log('Ürün sorgusu:', sql);
        const products = await firebird.query(sql);
        console.log('Sorgu sonucu:', products);
        
        // NULL olmayan alanları filtreleyelim
        const nonNullFields = Object.entries(products[0] || {})
            .filter(([key, value]) => value !== null && value !== undefined)
            .reduce((obj, [key, value]) => {
                obj[key] = value;
                return obj;
            }, {});
        
        return { 
            success: true, 
            message: 'Ürün detayları başarıyla getirildi',
            data: nonNullFields,
            tables: tables
        };
    } catch (error) {
        console.error('Ürün detayları getirilirken hata:', {
            message: error.message,
            stack: error.stack,
            code: error.code,
            sqlState: error.sqlState,
            gdscode: error.gdscode
        });
        throw new Error(`Ürün detayları getirilemedi: ${error.message}`);
    }
}

// Ürün stok miktarını getir
async function getProductStock(stokKodu) {
    try {
        const sql = `
            SELECT 
                D.DEPO_ADI,
                DSB.MIKTAR
            FROM DEPOLAR_STOK_BAKIYE DSB
            JOIN DEPOLAR D ON D.DEPO_KODU = DSB.DEPOKODU
            WHERE DSB.STOKKODU = ?
        `;
        
        const result = await firebird.query(sql, [stokKodu]);
        return { success: true, data: result };
    } catch (error) {
        console.error('Stok miktarı alınırken hata:', error);
        throw new Error('Stok miktarı alınamadı.');
    }
}

// Ürün fiyatını getir
async function getProductPrice(stokKodu) {
    try {
        const sql = `
            SELECT 
                R.RDB$FIELD_NAME as COLUMN_NAME,
                F.RDB$FIELD_LENGTH as FIELD_LENGTH,
                F.RDB$FIELD_PRECISION as FIELD_PRECISION,
                F.RDB$FIELD_SCALE as FIELD_SCALE,
                F.RDB$FIELD_TYPE as FIELD_TYPE,
                R.RDB$NULL_FLAG as IS_NOT_NULL
            FROM RDB$RELATION_FIELDS R
            JOIN RDB$FIELDS F ON R.RDB$FIELD_SOURCE = F.RDB$FIELD_NAME
            WHERE R.RDB$RELATION_NAME = 'STOK_DEPO'
            ORDER BY R.RDB$FIELD_POSITION
        `;
        
        const result = await firebird.query(sql, [stokKodu]);
        return { success: true, data: result };
    } catch (error) {
        console.error('Fiyat bilgisi alınırken hata:', error);
        throw new Error('Fiyat bilgisi alınamadı.');
    }
}

// Ürün resimlerini getir
async function getProductImages(stokKodu) {
    try {
        const sql = `
            SELECT 
                RESIM,
                RESIM2,
                RESIM3,
                RESIM4,
                RESIM5
            FROM STOKLAR
            WHERE STOK_KODU = ?
        `;
        
        const result = await firebird.query(sql, [stokKodu]);
        
        if (result.length === 0) {
            return { success: true, data: [] };
        }
        
        const images = Object.values(result[0])
            .filter(image => image && image.trim())
            .map(image => image.trim());
        
        return { success: true, data: images };
    } catch (error) {
        console.error('Resimler alınırken hata:', error);
        throw new Error('Resimler alınamadı.');
    }
}

// Stok bilgilerini getir
async function getStockLevels() {
    try {
        const sql = `
            SELECT FIRST 100
                S.STOK_KODU,
                S.STOK_ADI,
                D.DEPO_KODU,
                D.DEPO_ADI,
                SD.MIKTAR
            FROM STOKLAR S
            LEFT JOIN STOK_DEPO_MIKTAR SD ON S.STOK_KODU = SD.STOK_KODU
            LEFT JOIN DEPOLAR D ON SD.DEPO_KODU = D.DEPO_KODU
            WHERE S.AKTIF = 'E'
        `;
        
        const stockLevels = await firebird.query(sql);
        return { success: true, data: stockLevels };
    } catch (error) {
        console.error('Stok seviyeleri getirilirken hata:', error);
        throw new Error('Stok seviyeleri getirilemedi.');
    }
}

// Siparişleri getir
async function getOrders(startDate, endDate, status) {
    try {
        const sql = `
            SELECT FIRST 100
                SH.FATURA_NO,
                SH.TARIH,
                SH.CARI_KOD,
                C.CARI_ISIM,
                SH.TOPLAM_TUTAR,
                SH.TOPLAM_KDV,
                SH.GENEL_TOPLAM
            FROM SATIS_FATURALARI SH
            LEFT JOIN CARI_HESAPLAR C ON SH.CARI_KOD = C.CARI_KOD
            WHERE SH.TARIH BETWEEN ? AND ?
            ${status ? "AND SH.DURUM = ?" : ""}
            ORDER BY SH.TARIH DESC
        `;
        
        const params = [startDate, endDate];
        if (status) params.push(status);
        
        const orders = await firebird.query(sql, params);
        return { success: true, data: orders };
    } catch (error) {
        console.error('Siparişler getirilirken hata:', error);
        throw new Error('Siparişler getirilemedi.');
    }
}

module.exports = {
    saveConnectionSettings,
    testConnection,
    getProducts,
    getStockLevels,
    getOrders,
    getProductStock,
    getProductImages,
    getProductPrice
}; 