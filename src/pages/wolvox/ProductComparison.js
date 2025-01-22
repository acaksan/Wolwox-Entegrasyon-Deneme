import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Button,
  CircularProgress,
  Typography,
  Grid
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';

const ProductComparison = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/wolvox/products/comparison');
      const data = await response.json();
      if (data.success) {
        setProducts(data.products);
      } else {
        console.error('Ürünler getirilemedi:', data.error);
      }
    } catch (error) {
      console.error('API hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredProducts = () => {
    return products.filter(product => {
      const matchesSearch = 
        product.wolvoxCode?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.wolvoxName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.wooCode?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.wooName?.toLowerCase().includes(searchTerm.toLowerCase());

      if (!matchesSearch) return false;

      switch (filter) {
        case 'matched':
          return product.isMatched;
        case 'unmatched':
          return !product.isMatched;
        case 'price':
          return product.hasPriceDiff;
        case 'stock':
          return product.hasStockDiff;
        default:
          return true;
      }
    });
  };

  const getStatusChip = (product) => {
    if (!product.isMatched) {
      return <Chip label="Eşleşmedi" color="error" size="small" />;
    }
    if (product.hasPriceDiff || product.hasStockDiff) {
      return <Chip label="Farklılık Var" color="warning" size="small" />;
    }
    return <Chip label="Eşleşti" color="success" size="small" />;
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Ürün Karşılaştırma
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Ürün Ara"
            variant="outlined"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
            }}
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Filtrele</InputLabel>
            <Select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              label="Filtrele"
              startAdornment={<FilterListIcon sx={{ mr: 1, color: 'text.secondary' }} />}
            >
              <MenuItem value="all">Tüm Ürünler</MenuItem>
              <MenuItem value="matched">Eşleşenler</MenuItem>
              <MenuItem value="unmatched">Eşleşmeyenler</MenuItem>
              <MenuItem value="price">Fiyat Farklılığı</MenuItem>
              <MenuItem value="stock">Stok Farklılığı</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <Button
            fullWidth
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchProducts}
            disabled={loading}
          >
            Yenile
          </Button>
        </Grid>
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Durum</TableCell>
              <TableCell>Wolvox Kodu</TableCell>
              <TableCell>Wolvox Adı</TableCell>
              <TableCell>Wolvox Fiyat</TableCell>
              <TableCell>Wolvox Stok</TableCell>
              <TableCell>WooCommerce Kodu</TableCell>
              <TableCell>WooCommerce Adı</TableCell>
              <TableCell>WooCommerce Fiyat</TableCell>
              <TableCell>WooCommerce Stok</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={9} align="center">
                  <CircularProgress />
                </TableCell>
              </TableRow>
            ) : getFilteredProducts().map((product) => (
              <TableRow key={product.wolvoxCode}>
                <TableCell>{getStatusChip(product)}</TableCell>
                <TableCell>{product.wolvoxCode}</TableCell>
                <TableCell>{product.wolvoxName}</TableCell>
                <TableCell>{product.wolvoxPrice?.toFixed(2)} TL</TableCell>
                <TableCell>{product.wolvoxStock}</TableCell>
                <TableCell>{product.wooCode}</TableCell>
                <TableCell>{product.wooName}</TableCell>
                <TableCell>{product.wooPrice?.toFixed(2)} TL</TableCell>
                <TableCell>{product.wooStock}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ProductComparison; 