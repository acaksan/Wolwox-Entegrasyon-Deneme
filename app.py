from flask import Flask, render_template, jsonify, request
from wolvox_product import WolvoxProductReader
from config import *
import logging
from datetime import datetime
import os
import json
import fdb
from woocommerce import API

# Logs klasörünü oluştur
if not os.path.exists('logs'):
    os.makedirs('logs')

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('WolvoxApp')

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Güvenli bir anahtar kullanın

def get_products():
    """Tüm ürünleri getirir"""
    try:
        reader = WolvoxProductReader()
        products = reader.get_all_products()
        
        # Her ürün için stok miktarını al
        for product in products:
            product['stok_miktari'] = reader.get_product_stock(product['stok_kodu'])
            product['resimler'] = reader.get_product_images(product['stok_kodu'])
        
        reader.close()
        return products
        
    except Exception as e:
        logger.error(f"Ürün verisi çekme hatası: {str(e)}")
        return []

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/products')
def products():
    """Ürün verilerini JSON olarak döndürür"""
    products = get_products()
    return jsonify(products)

@app.route('/api/settings/woocommerce', methods=['GET'])
def get_woocommerce_settings():
    """WooCommerce ayarlarını döndürür"""
    return jsonify({
        'url': WC_URL,
        'consumer_key': WC_CONSUMER_KEY,
        'consumer_secret': WC_CONSUMER_SECRET,
        'version': WC_VERSION
    })

@app.route('/api/settings/woocommerce', methods=['POST'])
def save_woocommerce_settings():
    """WooCommerce ayarlarını kaydeder"""
    try:
        data = request.get_json()
        
        # config.py dosyasını güncelle
        with open('config.py', 'r', encoding='utf-8') as f:
            config = f.read()
        
        # Değerleri güncelle
        config = config.replace(f"WC_URL = '{WC_URL}'", f"WC_URL = '{data['url']}'")
        config = config.replace(f"WC_CONSUMER_KEY = '{WC_CONSUMER_KEY}'", f"WC_CONSUMER_KEY = '{data['consumer_key']}'")
        config = config.replace(f"WC_CONSUMER_SECRET = '{WC_CONSUMER_SECRET}'", f"WC_CONSUMER_SECRET = '{data['consumer_secret']}'")
        config = config.replace(f"WC_VERSION = '{WC_VERSION}'", f"WC_VERSION = '{data['version']}'")
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config)
        
        return jsonify({'success': True, 'message': 'WooCommerce ayarları kaydedildi'})
    except Exception as e:
        logger.error(f"WooCommerce ayarları kaydedilirken hata: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/settings/database', methods=['GET'])
def get_database_settings():
    """Veritabanı ayarlarını döndürür"""
    return jsonify({
        'host': FB_HOST,
        'database': FB_DATABASE,
        'user': FB_USER,
        'password': FB_PASSWORD,
        'charset': FB_CHARSET,
        'port': FB_PORT
    })

@app.route('/api/settings/database', methods=['POST'])
def save_database_settings():
    """Veritabanı ayarlarını kaydeder"""
    try:
        data = request.get_json()
        
        # config.py dosyasını güncelle
        with open('config.py', 'r', encoding='utf-8') as f:
            config = f.read()
        
        # Değerleri güncelle
        config = config.replace(f"FB_HOST = '{FB_HOST}'", f"FB_HOST = '{data['host']}'")
        config = config.replace(f"FB_DATABASE = '{FB_DATABASE}'", f"FB_DATABASE = '{data['database']}'")
        config = config.replace(f"FB_USER = '{FB_USER}'", f"FB_USER = '{data['user']}'")
        config = config.replace(f"FB_PASSWORD = '{FB_PASSWORD}'", f"FB_PASSWORD = '{data['password']}'")
        config = config.replace(f"FB_CHARSET = '{FB_CHARSET}'", f"FB_CHARSET = '{data['charset']}'")
        config = config.replace(f"FB_PORT = {FB_PORT}", f"FB_PORT = {data['port']}")
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config)
        
        return jsonify({'success': True, 'message': 'Veritabanı ayarları kaydedildi'})
    except Exception as e:
        logger.error(f"Veritabanı ayarları kaydedilirken hata: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test/database', methods=['POST'])
def test_database_connection():
    """Veritabanı bağlantısını test eder"""
    try:
        data = request.get_json()
        conn = fdb.connect(
            host=data.get('host', FB_HOST),
            database=data.get('database', FB_DATABASE),
            user=data.get('user', FB_USER),
            password=data.get('password', FB_PASSWORD),
            charset=data.get('charset', FB_CHARSET),
            port=data.get('port', FB_PORT)
        )
        conn.close()
        return jsonify({'success': True, 'message': 'Veritabanı bağlantısı başarılı'})
    except Exception as e:
        logger.error(f"Veritabanı bağlantı testi hatası: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test/woocommerce', methods=['POST'])
def test_woocommerce_connection():
    """WooCommerce bağlantısını test eder"""
    try:
        data = request.get_json()
        wcapi = API(
            url=data.get('url', WC_URL),
            consumer_key=data.get('consumer_key', WC_CONSUMER_KEY),
            consumer_secret=data.get('consumer_secret', WC_CONSUMER_SECRET),
            version=data.get('version', WC_VERSION)
        )
        
        # Basit bir API çağrısı yap
        response = wcapi.get("products", params={"per_page": 1})
        
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'WooCommerce bağlantısı başarılı'})
        else:
            return jsonify({'success': False, 'message': f'WooCommerce bağlantı hatası: {response.status_code}'}), 500
            
    except Exception as e:
        logger.error(f"WooCommerce bağlantı testi hatası: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/categories/wolvox')
def get_wolvox_categories():
    """Wolvox kategorilerini getir"""
    try:
        wolvox = WolvoxProductReader()
        categories = wolvox.get_categories()
        wolvox.close()
        return jsonify(categories)
    except Exception as e:
        logger.error(f"Wolvox kategorileri alınırken hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/woocommerce')
def get_woocommerce_categories():
    """WooCommerce kategorilerini getir"""
    try:
        wcapi = API(
            url=WC_URL,
            consumer_key=WC_CONSUMER_KEY,
            consumer_secret=WC_CONSUMER_SECRET,
            version=WC_VERSION
        )
        
        # Tüm kategorileri al
        categories = []
        page = 1
        while True:
            response = wcapi.get("products/categories", params={"per_page": 100, "page": page})
            if response.status_code != 200:
                raise Exception(f"WooCommerce API hatası: {response.status_code}")
            
            data = response.json()
            if not data:
                break
                
            categories.extend(data)
            page += 1
        
        # Kategori ağacını oluştur
        category_tree = []
        category_map = {cat['id']: cat for cat in categories}
        
        for category in categories:
            if category['parent'] == 0:
                category_tree.append({
                    'id': category['id'],
                    'name': category['name'],
                    'slug': category['slug'],
                    'type': 'main',
                    'subcategories': []
                })
            else:
                parent = category_map.get(category['parent'])
                if parent:
                    parent_tree = next((cat for cat in category_tree if cat['id'] == parent['id']), None)
                    if parent_tree:
                        parent_tree['subcategories'].append({
                            'id': category['id'],
                            'name': category['name'],
                            'slug': category['slug'],
                            'type': 'sub',
                            'parent': parent['name']
                        })
        
        return jsonify(category_tree)
    except Exception as e:
        logger.error(f"WooCommerce kategorileri alınırken hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/woocommerce', methods=['POST'])
def create_woocommerce_category():
    """Yeni WooCommerce kategorisi oluştur"""
    try:
        wcapi = get_woocommerce_api()
        data = request.json
        response = wcapi.post("products/categories", data).json()
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/woocommerce/<int:category_id>', methods=['PUT'])
def update_woocommerce_category(category_id):
    """WooCommerce kategorisini güncelle"""
    try:
        wcapi = get_woocommerce_api()
        data = request.json
        response = wcapi.put(f"products/categories/{category_id}", data).json()
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/woocommerce/<int:category_id>', methods=['DELETE'])
def delete_woocommerce_category(category_id):
    """WooCommerce kategorisini sil"""
    try:
        wcapi = get_woocommerce_api()
        response = wcapi.delete(f"products/categories/{category_id}", params={"force": True}).json()
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/mapping')
def get_category_mappings():
    """Kategori eşleştirmelerini getir"""
    try:
        # TODO: Veritabanından kategori eşleştirmelerini getir
        mappings = []
        return jsonify(mappings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/mapping', methods=['POST'])
def create_category_mapping():
    """Yeni kategori eşleştirmesi oluştur"""
    try:
        data = request.json
        # TODO: Veritabanına kategori eşleştirmesini kaydet
        return jsonify({'success': True, 'id': 1})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/mapping/<int:mapping_id>', methods=['DELETE'])
def delete_category_mapping(mapping_id):
    """Kategori eşleştirmesini sil"""
    try:
        # TODO: Veritabanından kategori eşleştirmesini sil
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
