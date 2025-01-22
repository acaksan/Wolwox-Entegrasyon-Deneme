import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/MainLayout';

// Akınsoft Wolvox Entegrasyon Sayfaları
import WolvoxConnection from './pages/wolvox/WolvoxConnection';
import ProductSync from './pages/wolvox/ProductSync';
import StockSync from './pages/wolvox/StockSync';
import OrderSync from './pages/wolvox/OrderSync';

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

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          {/* Wolvox2 Rotaları */}
          <Route path="/wolvox/connection" element={<WolvoxConnection />} />
          <Route path="/wolvox/products" element={<ProductSync />} />
          <Route path="/wolvox/stock" element={<StockSync />} />
          <Route path="/wolvox/orders" element={<OrderSync />} />

          {/* WooCommerce Rotaları */}
          <Route path="/woocommerce/settings" element={<WooCommerceSettings />} />
          <Route path="/woocommerce/products" element={<WooProductSync />} />
          <Route path="/woocommerce/stock" element={<WooStockSync />} />
          <Route path="/woocommerce/orders" element={<WooOrderSync />} />

          {/* Ayarlar Rotaları */}
          <Route path="/settings/general" element={<GeneralSettings />} />
          <Route path="/settings/api" element={<ApiSettings />} />
          <Route path="/settings/logs" element={<SystemLogs />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App; 