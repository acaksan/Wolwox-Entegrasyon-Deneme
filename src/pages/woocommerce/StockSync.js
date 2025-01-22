import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Button,
  Typography,
  Alert,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  FormControlLabel,
  Checkbox,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

function StockSync() {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    logs: []
  });

  const [syncOptions, setSyncOptions] = useState({
    syncOutOfStock: true,
    syncBackorders: true,
    syncStockStatus: true,
    updateMode: 'all',
    notifyLowStock: true
  });

  const handleOptionChange = (event) => {
    const { name, checked, value } = event.target;
    setSyncOptions(prev => ({
      ...prev,
      [name]: event.target.type === 'checkbox' ? checked : value
    }));
  };

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'WooCommerce stok senkronizasyonu başlatılıyor...',
        logs: []
      });

      // API'ye senkronizasyon başlatma isteği gönder
      const response = await fetch('/api/woocommerce/sync-stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(syncOptions)
      });

      if (!response.ok) {
        throw new Error('Senkronizasyon başlatılamadı');
      }

      // Başarılı yanıt durumunda
      setSyncStatus(prev => ({
        ...prev,
        message: 'Stok senkronizasyonu başarıyla tamamlandı',
        isRunning: false,
        progress: 100,
        logs: [...prev.logs, 'Senkronizasyon tamamlandı']
      }));

    } catch (error) {
      setSyncStatus(prev => ({
        ...prev,
        isRunning: false,
        message: `Hata: ${error.message}`,
        logs: [...prev.logs, `Hata: ${error.message}`]
      }));
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            WooCommerce Stok Senkronizasyonu
          </Typography>

          <Box sx={{ my: 3 }}>
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
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncBackorders}
                  onChange={handleOptionChange}
                  name="syncBackorders"
                />
              }
              label="Ön Sipariş Durumlarını Senkronize Et"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncStockStatus}
                  onChange={handleOptionChange}
                  name="syncStockStatus"
                />
              }
              label="Stok Durumlarını Senkronize Et"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.notifyLowStock}
                  onChange={handleOptionChange}
                  name="notifyLowStock"
                />
              }
              label="Düşük Stok Bildirimi Gönder"
            />
          </Box>

          <Box sx={{ my: 3 }}>
            <FormControl fullWidth>
              <InputLabel>Güncelleme Modu</InputLabel>
              <Select
                value={syncOptions.updateMode}
                onChange={handleOptionChange}
                name="updateMode"
                label="Güncelleme Modu"
              >
                <MenuItem value="all">Tüm Ürünler</MenuItem>
                <MenuItem value="changed">Sadece Değişenler</MenuItem>
                <MenuItem value="lowStock">Sadece Düşük Stoklu Ürünler</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Box sx={{ my: 3 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleStartSync}
              disabled={syncStatus.isRunning}
            >
              Stok Senkronizasyonunu Başlat
            </Button>
          </Box>

          {syncStatus.isRunning && (
            <Box sx={{ width: '100%', mb: 2 }}>
              <LinearProgress variant="determinate" value={syncStatus.progress} />
            </Box>
          )}

          {syncStatus.message && (
            <Alert 
              severity={syncStatus.message.includes('Hata') ? 'error' : 'success'}
              sx={{ mb: 2 }}
            >
              {syncStatus.message}
            </Alert>
          )}

          {syncStatus.logs.length > 0 && (
            <>
              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                İşlem Kayıtları
              </Typography>
              <List>
                {syncStatus.logs.map((log, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemText primary={log} />
                    </ListItem>
                    {index < syncStatus.logs.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}

export default StockSync; 