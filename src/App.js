import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';

// Akınsoft Wolvox Entegrasyon Sayfaları
import WolvoxConnection from './pages/wolvox/WolvoxConnection';
import ProductSync from './pages/wolvox/ProductSync';
import StockSync from './pages/wolvox/StockSync';
import OrderSync from './pages/wolvox/OrderSync';
import ProductComparison from './pages/wolvox/ProductComparison';

// WooCommerce Entegrasyon Sayfaları
import WooCommerceSettings from './pages/woocommerce/WooCommerceSettings';
import WooProductSync from './pages/woocommerce/ProductSync';
import WooStockSync from './pages/woocommerce/StockSync';
import WooOrderSync from './pages/woocommerce/OrderSync';

// Ayarlar Sayfaları
import GeneralSettings from './pages/settings/GeneralSettings';
import ApiSettings from './pages/settings/ApiSettings';
import SystemLogs from './pages/settings/SystemLogs';

import './App.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          {/* Akınsoft Wolvox Rotaları */}
          <Route path="/wolvox/connection" element={<WolvoxConnection />} />
          <Route path="/wolvox/products" element={<ProductSync />} />
          <Route path="/wolvox/stock" element={<StockSync />} />
          <Route path="/wolvox/orders" element={<OrderSync />} />
          <Route path="/wolvox/comparison" element={<ProductComparison />} />
          
          {/* WooCommerce Rotaları */}
          <Route path="/woocommerce/settings" element={<WooCommerceSettings />} />
          <Route path="/woocommerce/products" element={<WooProductSync />} />
          <Route path="/woocommerce/stock" element={<WooStockSync />} />
          <Route path="/woocommerce/orders" element={<WooOrderSync />} />
          
          {/* Ana sayfa için varsayılan rota */}
          <Route index element={<WolvoxConnection />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App; 