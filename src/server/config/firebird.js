const Firebird = require('node-firebird');
require('dotenv').config();

const defaultOptions = {
    host: process.env.FIREBIRD_HOST || 'localhost',
    port: parseInt(process.env.FIREBIRD_PORT) || 3050,
    database: process.env.FIREBIRD_DATABASE,
    user: process.env.FIREBIRD_USER || 'SYSDBA',
    password: process.env.FIREBIRD_PASSWORD || 'masterkey',
    lowercase_keys: false,
    role: null,
    pageSize: parseInt(process.env.FIREBIRD_PAGE_SIZE) || 4096,
    retryConnectionInterval: parseInt(process.env.FIREBIRD_RETRY_INTERVAL) || 1000,
    charset: process.env.FIREBIRD_CHARSET || 'WIN1254',
    fbClientLibrary: process.env.FIREBIRD_CLIENT_LIBRARY
};

// Bağlantı havuzu oluştur
const poolSize = parseInt(process.env.FIREBIRD_POOL_SIZE) || 5;
const pool = Firebird.pool(poolSize, defaultOptions);

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

// Bağlantı durumunu kontrol et
async function checkConnection() {
    try {
        const connection = await getConnection();
        connection.detach();
        return true;
    } catch (error) {
        console.error('Bağlantı kontrol hatası:', error);
        return false;
    }
}

module.exports = {
    getConnection,
    query,
    testConnection,
    closePool,
    checkConnection,
    options: defaultOptions
}; 