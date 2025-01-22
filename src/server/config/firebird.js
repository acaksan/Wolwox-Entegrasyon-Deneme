const Firebird = require('node-firebird');

const defaultOptions = {
    host: 'localhost',
    port: 3050,
    database: 'D:\\AKINSOFT\\Wolvox8\\Database_FB\\DEMOWOLVOX\\2025\\WOLVOX.FDB', // Demo veritabanı yolu
    user: 'SYSDBA',
    password: 'masterkey',
    lowercase_keys: false,
    role: null,
    pageSize: 4096,
    retryConnectionInterval: 1000,
    charset: 'WIN1254', // Türkçe karakter desteği için
    fbClientLibrary: 'C:\\Program Files (x86)\\Firebird\\Firebird_2_5\\bin\\fbclient.dll' // 32 bit Firebird client
};

// Bağlantı havuzu oluştur
const pool = Firebird.pool(5, defaultOptions); // 5 eşzamanlı bağlantı

// Bağlantı al
function getConnection() {
    return new Promise((resolve, reject) => {
        pool.get((err, db) => {
            if (err) {
                console.error('Firebird bağlantı hatası:', err);
                reject(err);
                return;
            }
            resolve(db);
        });
    });
}

// Sorgu çalıştır
async function query(sql, params = []) {
    let connection;
    try {
        connection = await getConnection();
        return new Promise((resolve, reject) => {
            connection.query(sql, params, (err, result) => {
                if (err) {
                    console.error('Sorgu hatası:', err);
                    reject(err);
                    return;
                }
                resolve(result);
            });
        });
    } finally {
        if (connection) {
            connection.detach();
        }
    }
}

// Bağlantıyı test et
async function testConnection() {
    let connection;
    try {
        connection = await getConnection();
        // Tabloları listele
        await new Promise((resolve, reject) => {
            connection.query(`
                SELECT RDB$RELATION_NAME
                FROM RDB$RELATIONS
                WHERE RDB$SYSTEM_FLAG = 0
                AND RDB$RELATION_TYPE = 0
                ORDER BY RDB$RELATION_NAME
            `, [], (err, result) => {
                if (err) {
                    reject(err);
                    return;
                }
                console.log('Mevcut tablolar:', result.map(r => r.RDB$RELATION_NAME.trim()));
                resolve(result);
            });
        });
        return { success: true, message: 'Firebird bağlantısı başarılı' };
    } catch (error) {
        console.error('Firebird bağlantı testi hatası:', error);
        return { success: false, message: error.message };
    } finally {
        if (connection) {
            connection.detach();
        }
    }
}

// Havuzu kapat
function closePool() {
    return new Promise((resolve) => {
        pool.destroy(resolve);
    });
}

module.exports = {
    getConnection,
    query,
    testConnection,
    closePool,
    options: defaultOptions
}; 