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

function ProductSync() {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    logs: []
  });

  const [syncOptions, setSyncOptions] = useState({
    syncImages: true,
    syncCategories: true,
    syncAttributes: true,
    syncVariations: true,
    productStatus: 'publish',
    updateExisting: true
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
        message: 'WooCommerce ürün senkronizasyonu başlatılıyor...',
        logs: []
      });

      // API'ye senkronizasyon başlatma isteği gönder
      const response = await fetch('/api/woocommerce/sync-products', {
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
        message: 'Ürün senkronizasyonu başarıyla tamamlandı',
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
            WooCommerce Ürün Senkronizasyonu
          </Typography>

          <Box sx={{ my: 3 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncImages}
                  onChange={handleOptionChange}
                  name="syncImages"
                />
              }
              label="Ürün Görsellerini Senkronize Et"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncCategories}
                  onChange={handleOptionChange}
                  name="syncCategories"
                />
              }
              label="Kategorileri Senkronize Et"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncAttributes}
                  onChange={handleOptionChange}
                  name="syncAttributes"
                />
              }
              label="Özellikleri Senkronize Et"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncVariations}
                  onChange={handleOptionChange}
                  name="syncVariations"
                />
              }
              label="Varyasyonları Senkronize Et"
            />
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
          </Box>

          <Box sx={{ my: 3 }}>
            <FormControl fullWidth>
              <InputLabel>Ürün Durumu</InputLabel>
              <Select
                value={syncOptions.productStatus}
                onChange={handleOptionChange}
                name="productStatus"
                label="Ürün Durumu"
              >
                <MenuItem value="publish">Yayında</MenuItem>
                <MenuItem value="draft">Taslak</MenuItem>
                <MenuItem value="private">Gizli</MenuItem>
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
              Ürün Senkronizasyonunu Başlat
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

export default ProductSync; 