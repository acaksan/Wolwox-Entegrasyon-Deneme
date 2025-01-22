import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Button,
  Typography,
  Alert,
  LinearProgress,
  FormControlLabel,
  Checkbox,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

const ProductSync = () => {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    success: null
  });

  const [syncOptions, setSyncOptions] = useState({
    syncImages: true,
    syncCategories: true,
    syncAttributes: true,
    syncVariations: true,
    updateExisting: true,
    productStatus: 'publish'
  });

  const handleOptionChange = (event) => {
    setSyncOptions({
      ...syncOptions,
      [event.target.name]: event.target.checked
    });
  };

  const handleStatusChange = (event) => {
    setSyncOptions({
      ...syncOptions,
      productStatus: event.target.value
    });
  };

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'Ürün senkronizasyonu başlatılıyor...',
        success: null
      });

      const response = await fetch('/api/woocommerce/products/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(syncOptions)
      });

      const result = await response.json();

      setSyncStatus({
        isRunning: false,
        progress: 100,
        message: result.message,
        success: result.success
      });
    } catch (error) {
      setSyncStatus({
        isRunning: false,
        progress: 0,
        message: 'Senkronizasyon sırasında hata oluştu: ' + error.message,
        success: false
      });
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            WooCommerce Ürün Aktarımı
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncImages}
                    onChange={handleOptionChange}
                    name="syncImages"
                  />
                }
                label="Ürün Görsellerini Aktar"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncCategories}
                    onChange={handleOptionChange}
                    name="syncCategories"
                  />
                }
                label="Kategorileri Aktar"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncAttributes}
                    onChange={handleOptionChange}
                    name="syncAttributes"
                  />
                }
                label="Özellikleri Aktar"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncVariations}
                    onChange={handleOptionChange}
                    name="syncVariations"
                  />
                }
                label="Varyasyonları Aktar"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.updateExisting}
                    onChange={handleOptionChange}
                    name="updateExisting"
                  />
                }
                label="Mevcut Ürünleri Güncelle"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Ürün Durumu</InputLabel>
                <Select
                  value={syncOptions.productStatus}
                  onChange={handleStatusChange}
                  label="Ürün Durumu"
                >
                  <MenuItem value="publish">Yayında</MenuItem>
                  <MenuItem value="draft">Taslak</MenuItem>
                  <MenuItem value="private">Özel</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleStartSync}
              disabled={syncStatus.isRunning}
            >
              {syncStatus.isRunning ? 'Aktarım Devam Ediyor...' : 'Aktarımı Başlat'}
            </Button>
          </Box>

          {syncStatus.isRunning && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress variant="determinate" value={syncStatus.progress} />
              <Typography variant="body2" sx={{ mt: 1 }}>
                {syncStatus.message}
              </Typography>
            </Box>
          )}

          {syncStatus.success !== null && !syncStatus.isRunning && (
            <Alert 
              severity={syncStatus.success ? "success" : "error"}
              sx={{ mt: 2 }}
            >
              {syncStatus.message}
            </Alert>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProductSync; 