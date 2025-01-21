import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';

// Products
import ProductList from './pages/products/ProductList';
import AddProduct from './pages/products/AddProduct';
import BulkOperations from './pages/products/BulkOperations';
import ImportExport from './pages/products/ImportExport';

// Categories
import CategoryTree from './pages/categories/CategoryTree';
import CategoryMapping from './pages/categories/CategoryMapping';
import CategoryTemplates from './pages/categories/CategoryTemplates';

// Tire Specs
import Dimensions from './pages/tire-specs/Dimensions';
import Seasons from './pages/tire-specs/Seasons';
import SpeedCodes from './pages/tire-specs/SpeedCodes';
import LoadIndexes from './pages/tire-specs/LoadIndexes';
import SpecSets from './pages/tire-specs/SpecSets';

import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          {/* Ana sayfa yönlendirmesi */}
          <Route index element={<Navigate to="/products/list" replace />} />

          {/* Products Routes */}
          <Route path="/products/list" element={<ProductList />} />
          <Route path="/products/add" element={<AddProduct />} />
          <Route path="/products/bulk" element={<BulkOperations />} />
          <Route path="/products/import-export" element={<ImportExport />} />

          {/* Categories Routes */}
          <Route path="/categories/tree" element={<CategoryTree />} />
          <Route path="/categories/mapping" element={<CategoryMapping />} />
          <Route path="/categories/templates" element={<CategoryTemplates />} />

          {/* Tire Specs Routes */}
          <Route path="/tire-specs/dimensions" element={<Dimensions />} />
          <Route path="/tire-specs/seasons" element={<Seasons />} />
          <Route path="/tire-specs/speed-codes" element={<SpeedCodes />} />
          <Route path="/tire-specs/load-indexes" element={<LoadIndexes />} />
          <Route path="/tire-specs/spec-sets" element={<SpecSets />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App; 