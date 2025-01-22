const firebird = require('../config/firebird');
const WooCommerceAPI = require('@woocommerce/woocommerce-rest-api').default;

const wooCommerce = new WooCommerceAPI({
  url: process.env.WOOCOMMERCE_URL,
  consumerKey: process.env.WOOCOMMERCE_KEY,
  consumerSecret: process.env.WOOCOMMERCE_SECRET,
  version: 'wc/v3'
});

const getProductComparison = async (req, res) => {
  try {
    console.log('Ürün karşılaştırması başlatılıyor...');

    // 1. Wolvox'tan ürünleri al
    const wolvoxProducts = await getWolvoxProducts();
    console.log(`${wolvoxProducts.length} adet Wolvox ürünü bulundu`);

    // 2. WooCommerce'den ürünleri al
    const wooProducts = await getWooCommerceProducts();
    console.log(`${wooProducts.length} adet WooCommerce ürünü bulundu`);

    // 3. Ürünleri karşılaştır
    const comparisonResults = compareProducts(wolvoxProducts, wooProducts);

    res.json({
      success: true,
      products: comparisonResults
    });

  } catch (error) {
    console.error('Ürün karşılaştırma hatası:', error);
    res.status(500).json({
      success: false,
      error: 'Ürün karşılaştırma işlemi başarısız oldu'
    });
  }
};

const getWolvoxProducts = async () => {
  const query = `
    SELECT 
      s.STOKKODU as wolvoxCode,
      s.STOK_ADI as wolvoxName,
      s.SATIS_FIYATI as wolvoxPrice,
      s.WEBDE_GORUNSUN as isVisible,
      s.AKTIF as isActive
    FROM STOK s
    WHERE s.WEBDE_GORUNSUN = 1 
    AND s.AKTIF = 1
  `;

  try {
    const products = await firebird.query(query);
    
    // Stok miktarlarını al
    for (let product of products) {
      const stockQuery = `
        SELECT SUM(MIKTAR) as totalStock
        FROM STOK_HAREKETLERI
        WHERE BLSTKODU = (
          SELECT BLKODU 
          FROM STOK 
          WHERE STOKKODU = '${product.wolvoxCode}'
        )
      `;
      
      const [stockResult] = await firebird.query(stockQuery);
      product.wolvoxStock = stockResult?.TOTALSTOCK || 0;
    }

    return products;
  } catch (error) {
    console.error('Wolvox ürünleri alınırken hata:', error);
    throw error;
  }
};

const getWooCommerceProducts = async () => {
  try {
    const { data } = await wooCommerce.get('products', {
      per_page: 100,
      status: 'publish'
    });

    return data.map(product => ({
      wooCode: product.sku,
      wooName: product.name,
      wooPrice: parseFloat(product.price),
      wooStock: product.stock_quantity
    }));
  } catch (error) {
    console.error('WooCommerce ürünleri alınırken hata:', error);
    throw error;
  }
};

const compareProducts = (wolvoxProducts, wooProducts) => {
  return wolvoxProducts.map(wolvoxProduct => {
    const wooProduct = wooProducts.find(wp => wp.wooCode === wolvoxProduct.wolvoxCode);
    
    if (!wooProduct) {
      return {
        ...wolvoxProduct,
        isMatched: false,
        hasPriceDiff: false,
        hasStockDiff: false
      };
    }

    const priceDiff = Math.abs(wolvoxProduct.wolvoxPrice - wooProduct.wooPrice) > 0.01;
    const stockDiff = wolvoxProduct.wolvoxStock !== wooProduct.wooStock;

    return {
      ...wolvoxProduct,
      ...wooProduct,
      isMatched: true,
      hasPriceDiff: priceDiff,
      hasStockDiff: stockDiff
    };
  });
};

module.exports = {
  getProductComparison
}; 