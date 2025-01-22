const Firebird = require('node-firebird');
const config = require('../config/firebird');

// Bağlantı ayarlarını kaydet
async function saveConnectionSettings(settings) {
    try {
        // Ayarları doğrula
        if (!settings.host || !settings.database || !settings.user || !settings.password) {
            throw new Error('Tüm bağlantı bilgileri gereklidir');
        }
        
        return {
            success: true,
            message: 'Bağlantı ayarları kaydedildi'
        };
    } catch (error) {
        console.error('Bağlantı ayarları kaydedilirken hata:', error);
        throw error;
    }
}

// Bağlantıyı test et
async function testConnection(settings) {
    let connection;
    try {
        // Ayarları doğrula
        if (!settings || !settings.host || !settings.database || !settings.username || !settings.password) {
            throw new Error('Tüm bağlantı bilgileri gereklidir');
        }

        // Test için yeni bir bağlantı oluştur
        const testOptions = {
            host: settings.host,
            port: parseInt(settings.port) || 3050,
            database: settings.database,
            user: settings.username,
            password: settings.password,
            charset: settings.charset || 'WIN1254'
        };

        // Bağlantıyı test et
        connection = await new Promise((resolve, reject) => {
            Firebird.attach(testOptions, (err, db) => {
                if (err) {
                    console.error('Bağlantı hatası:', err);
                    reject(err);
                    return;
                }
                resolve(db);
            });
        });

        // Basit bir sorgu dene
        await new Promise((resolve, reject) => {
            connection.query('SELECT 1 FROM RDB$DATABASE', [], (err, result) => {
                if (err) {
                    reject(err);
                    return;
                }
                resolve(result);
            });
        });
        
        return {
            success: true,
            message: 'Bağlantı başarılı'
        };
    } catch (error) {
        console.error('Bağlantı testi hatası:', error);
        return {
            success: false,
            message: 'Bağlantı başarısız: ' + error.message
        };
    } finally {
        if (connection) {
            connection.detach();
        }
    }
}

// Ürün listesini getir
async function getProducts() {
    try {
        console.log('Ürün detayları getiriliyor...');
        
        // Belirli stok kodlu ürünü getirelim ve NULL olmayan alanları gösterelim
        const sql = `
            SELECT FIRST 1 A.*, 
                   (SELECT LIST(TRIM(R.RDB$FIELD_NAME)) 
                    FROM RDB$RELATION_FIELDS R 
                    WHERE R.RDB$RELATION_NAME = 'STOK' 
                    AND R.RDB$FIELD_SOURCE IS NOT NULL 
                    AND (SELECT F.RDB$NULL_FLAG 
                         FROM RDB$FIELDS F 
                         WHERE F.RDB$FIELD_NAME = R.RDB$FIELD_SOURCE) = 1) as ZORUNLU_ALANLAR
            FROM STOK A
            WHERE A.STOKKODU = 'PET-100-70-13-175-4000'
        `;
        
        console.log('SQL Sorgusu:', sql);
        const products = await config.query(sql);
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
            zorunluAlanlar: products[0]?.ZORUNLU_ALANLAR
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
    console.log('Stok miktarı getiriliyor:', stokKodu);
    
    // Önce ürünün BLKODU'nu alalım
    const blkoduQuery = `SELECT BLKODU FROM STOK WHERE STOKKODU = ?`;
    const blkoduResult = await config.query(blkoduQuery, [stokKodu]);
    
    if (!blkoduResult || blkoduResult.length === 0) {
      return {
        success: false,
        message: 'Ürün bulunamadı',
        data: null
      };
    }
    
    const blkodu = blkoduResult[0].BLKODU;
    const depolar = ['1_AC AKSAN', '2_LASTIK VS', '3_CADDE SUBE'];
    
    // Depo bazında stok miktarlarını alalım
    const sql = `
      SELECT 
        sh.DEPO_ADI,
        SUM(CASE 
          WHEN sh.TUTAR_TURU = 0 THEN -sh.MIKTARI 
          WHEN sh.TUTAR_TURU = 1 THEN sh.MIKTARI 
          ELSE 0 
        END) as MIKTAR
      FROM STOKHR sh
      WHERE sh.BLSTKODU = ?
      AND sh.SILINDI = 0
      AND sh.DEPO_ADI IN (?, ?, ?)
      GROUP BY sh.DEPO_ADI
      ORDER BY sh.DEPO_ADI`;
    
    console.log('SQL Sorgusu:', sql);
    const result = await config.query(sql, [blkodu, ...depolar]);
    console.log('Stok bilgisi:', result);
    
    if (result && result.length > 0) {
      const stockInfo = result.map(row => ({
        depoAdi: row.DEPO_ADI ? row.DEPO_ADI.trim() : '',
        miktar: parseInt(row.MIKTAR) || 0
      }));
      
      // Tüm depoların toplamını hesapla
      const toplamStok = stockInfo.reduce((toplam, depo) => toplam + depo.miktar, 0);
      
      return {
        success: true,
        message: 'Stok miktarları başarıyla getirildi',
        data: {
          stokKodu,
          depolar: stockInfo,
          toplamStok: toplamStok // Tüm depoların toplamı (eksi stoklar dahil)
        }
      };
    } else {
      return {
        success: false,
        message: 'Stok bilgisi bulunamadı',
        data: {
          stokKodu,
          depolar: [],
          toplamStok: 0
        }
      };
    }
  } catch (error) {
    console.error('Stok miktarı alınırken hata:', error);
    return {
      success: false,
      message: 'Stok miktarı alınamadı',
      error: error.message
    };
  }
}

// Tüm ürünlerin stok miktarlarını getir
async function getAllProductsStock() {
  try {
    console.log('Stok ile ilgili tablolar aranıyor...');
    
    // Stok ile ilgili tabloları bulalım
    const tableQuery = `
      SELECT RDB$RELATION_NAME as TABLE_NAME
      FROM RDB$RELATIONS
      WHERE RDB$SYSTEM_FLAG = 0
      AND RDB$VIEW_BLR IS NULL
      AND (RDB$RELATION_NAME LIKE '%STOK%' OR RDB$RELATION_NAME LIKE '%STK%')
      ORDER BY RDB$RELATION_NAME`;
    
    console.log('Tablo arama sorgusu:', tableQuery);
    const tables = await config.query(tableQuery);
    console.log('Bulunan tablolar:', tables);
    
    // Aktif ürünleri getirelim
    const sql = `
      SELECT 
        s.STOKKODU,
        s.STOK_ADI,
        s.BARKODU,
        s.BLKODU,
        s.WEBDE_GORUNSUN,
        s.AKTIF
      FROM STOK s
      WHERE s.WEBDE_GORUNSUN = 1 AND s.AKTIF = 1
      ORDER BY s.STOKKODU`;
    
    console.log('Stok sorgusu:', sql);
    const result = await config.query(sql);
    console.log('Stok bilgileri:', result);
    
    if (result && result.length > 0) {
      const stockInfo = result.map(row => ({
        stokKodu: row.STOKKODU ? row.STOKKODU.trim() : '',
        stokAdi: row.STOK_ADI ? row.STOK_ADI.trim() : '',
        barkod: row.BARKODU ? row.BARKODU.trim() : '',
        blkodu: row.BLKODU,
        webdeGorunsun: row.WEBDE_GORUNSUN,
        aktif: row.AKTIF
      }));
      
      return {
        success: true,
        message: 'Stok bilgileri başarıyla getirildi',
        data: {
          tables: tables.map(t => t.TABLE_NAME.trim()),
          stocks: stockInfo
        }
      };
    } else {
      return {
        success: false,
        message: 'Hiç ürün bulunamadı',
        data: {
          tables: tables.map(t => t.TABLE_NAME.trim()),
          stocks: []
        }
      };
    }
  } catch (error) {
    console.error('Stok bilgileri alınırken hata:', error);
    return {
      success: false,
      message: 'Stok bilgileri alınamadı',
      error: error.message
    };
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
        
        const result = await config.query(sql, [stokKodu]);
        
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
        
        const stockLevels = await config.query(sql);
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
        
        const orders = await config.query(sql, params);
        return { success: true, data: orders };
    } catch (error) {
        console.error('Siparişler getirilirken hata:', error);
        throw new Error('Siparişler getirilemedi.');
    }
}

// Ürün fiyat bilgisini getir
async function getProductPrice() {
    try {
        console.log('Fiyat bilgisi aranıyor...');
        
        const sql = `
            SELECT A.*, B.STOK_ADI, B.STOKKODU, C.LISTE_ADI, C.LISTE_NO
            FROM STOK_FIYAT_LISTE_DT A
            LEFT JOIN STOK B ON A.BLSTKODU = B.BLKODU
            LEFT JOIN STOK_FIYAT_LISTE C ON A.BLFYTLISTE = C.BLKODU
            WHERE B.BLKODU = 21036
            ORDER BY C.LISTE_NO
        `;
        
        console.log('SQL Sorgusu:', sql);
        const prices = await config.query(sql);
        console.log('Sorgu sonucu:', prices);
        
        return { 
            success: true, 
            message: 'Fiyat bilgisi başarıyla getirildi',
            data: prices
        };
    } catch (error) {
        console.error('Fiyat bilgisi getirilirken hata:', {
            message: error.message,
            stack: error.stack,
            code: error.code,
            sqlState: error.sqlState,
            gdscode: error.gdscode
        });
        throw new Error(`Fiyat bilgisi getirilemedi: ${error.message}`);
    }
}

const getProductPrices = async () => {
  try {
    console.log('Ürün fiyatları getiriliyor...');
    
    // Birden fazla ürün kodu için sorgu
    const urunKodlari = [
      'PET-100-70-13-175-6000',
      'PET-100-70-13-175-4000',
      'PET-100-70-13-175-1000',
      'PET-100-70-13-175-5000',
      'PET-100-70-13-175-2000',
      'PET-100-70-13-175-6050'
    ];

    const placeholders = urunKodlari.map(() => '?').join(',');
    
    const sql = `
      SELECT s.STOKKODU, s.STOK_ADI, s.BARKODU, MAX(sf.FIYATI) as SATIS_FIYATI
      FROM STOK s
      JOIN STOK_FIYAT sf ON s.BLKODU = sf.BLSTKODU
      WHERE s.STOKKODU IN (${placeholders})
      AND sf.FIYAT_NO = 1
      GROUP BY s.STOKKODU, s.STOK_ADI, s.BARKODU
      ORDER BY s.STOKKODU`;
    
    console.log('SQL Sorgusu:', sql);
    console.log('Ürün Kodları:', urunKodlari);
    
    const prices = await config.query(sql, urunKodlari);
    console.log('Fiyat bilgileri:', prices);
    
    if (prices && prices.length > 0) {
      // Fiyat bilgilerini formatla
      const formattedPrices = prices.map(row => ({
        stokKodu: row.STOKKODU ? row.STOKKODU.trim() : '',
        stokAdi: row.STOK_ADI ? row.STOK_ADI.trim() : '',
        barkod: row.BARKODU ? row.BARKODU.trim() : '',
        satisFiyati: row.SATIS_FIYATI ? parseFloat(row.SATIS_FIYATI) : 0
      }));

      return {
        success: true,
        message: 'Fiyat bilgileri başarıyla getirildi',
        data: formattedPrices
      };
    } else {
      return {
        success: false,
        message: 'Ürünler için fiyat bilgisi bulunamadı',
        data: []
      };
    }
  } catch (error) {
    console.error('Fiyat bilgileri getirilemedi:', error);
    return {
      success: false,
      message: 'Fiyat bilgileri getirilemedi',
      error: error.message
    };
  }
};

module.exports = {
    saveConnectionSettings,
    testConnection,
    getProducts,
    getStockLevels,
    getOrders,
    getProductStock,
    getProductImages,
    getProductPrice,
    getProductPrices,
    getAllProductsStock
}; 