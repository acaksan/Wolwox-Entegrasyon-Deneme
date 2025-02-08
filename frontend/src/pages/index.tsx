import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Wolvox WooCommerce Entegrasyonu</title>
        <meta name="description" content="Wolvox ERP ve WooCommerce entegrasyonu yönetim paneli" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Wolvox WooCommerce Entegrasyonu
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Ürün Senkronizasyonu Kartı */}
          <Link href="/products">
            <div className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Ürün Senkronizasyonu</h2>
              <p className="text-gray-600 mb-4">
                Wolvox ve WooCommerce arasında ürün bilgilerini senkronize edin.
              </p>
              <span className="text-blue-500 hover:text-blue-600">
                Ürünleri Yönet →
              </span>
            </div>
          </Link>

          {/* Sipariş Yönetimi Kartı */}
          <Link href="/orders">
            <div className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Sipariş Yönetimi</h2>
              <p className="text-gray-600 mb-4">
                WooCommerce siparişlerini görüntüleyin ve Wolvox'a aktarın.
              </p>
              <span className="text-green-500 hover:text-green-600">
                Siparişleri Yönet →
              </span>
            </div>
          </Link>

          {/* Stok Takibi Kartı */}
          <Link href="/stock">
            <div className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Stok Takibi</h2>
              <p className="text-gray-600 mb-4">
                Wolvox ve WooCommerce stok durumlarını kontrol edin ve yönetin.
              </p>
              <span className="text-purple-500 hover:text-purple-600">
                Stokları Yönet →
              </span>
            </div>
          </Link>
        </div>
      </main>
    </div>
  );
};

export default Home;
