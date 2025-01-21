from flask import Blueprint, jsonify
from src.core.wolvox import WolvoxConnector
from src.core.woocommerce import WooCommerceSync

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products/sync-status')
def sync_status():
    """Senkronizasyon durumunu kontrol et"""
    try:
        # Mevcut bağlantıları kullan
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500 