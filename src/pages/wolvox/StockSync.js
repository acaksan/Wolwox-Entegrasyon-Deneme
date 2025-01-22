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
  Grid
} from '@mui/material';

const StockSync = () => {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    success: null
  });

  const [syncOptions, setSyncOptions] = useState({
    syncOutOfStock: true,
    syncBackorders: true,
    syncStockStatus: true,
    syncLowStockAmount: true,
    updateMode: 'replace' // 'replace' veya 'add'
  });

  const handleOptionChange = (event) => {
    setSyncOptions({
      ...syncOptions,
      [event.target.name]: event.target.checked
    });
  };

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'Stok senkronizasyonu başlatılıyor...',
        success: null
      });

      const response = await fetch('/api/woocommerce/stock/sync', {
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
            WooCommerce Stok Senkronizasyonu
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncOutOfStock}
                    onChange={handleOptionChange}
                    name="syncOutOfStock"
                  />
                }
                label="Stokta Olmayan Ürünleri Senkronize Et"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncBackorders}
                    onChange={handleOptionChange}
                    name="syncBackorders"
                  />
                }
                label="Ön Sipariş Durumunu Senkronize Et"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncStockStatus}
                    onChange={handleOptionChange}
                    name="syncStockStatus"
                  />
                }
                label="Stok Durumunu Senkronize Et"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={syncOptions.syncLowStockAmount}
                    onChange={handleOptionChange}
                    name="syncLowStockAmount"
                  />
                }
                label="Düşük Stok Bildirimlerini Senkronize Et"
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleStartSync}
              disabled={syncStatus.isRunning}
            >
              {syncStatus.isRunning ? 'Senkronizasyon Devam Ediyor...' : 'Senkronizasyonu Başlat'}
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

export default StockSync; 