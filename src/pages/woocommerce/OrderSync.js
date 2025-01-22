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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  FormControlLabel,
  Checkbox
} from '@mui/material';

function OrderSync() {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    logs: []
  });

  const [syncOptions, setSyncOptions] = useState({
    orderStatus: 'all',
    dateRange: {
      startDate: '',
      endDate: ''
    },
    syncCustomerData: true,
    syncShippingDetails: true,
    autoUpdateStatus: true,
    notifyCustomers: true
  });

  const handleOrderStatusChange = (event) => {
    setSyncOptions(prev => ({
      ...prev,
      orderStatus: event.target.value
    }));
  };

  const handleDateChange = (event) => {
    const { name, value } = event.target;
    setSyncOptions(prev => ({
      ...prev,
      dateRange: {
        ...prev.dateRange,
        [name]: value
      }
    }));
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setSyncOptions(prev => ({
      ...prev,
      [name]: checked
    }));
  };

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'WooCommerce sipariş senkronizasyonu başlatılıyor...',
        logs: []
      });

      // API'ye senkronizasyon başlatma isteği gönder
      const response = await fetch('/api/woocommerce/sync-orders', {
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
        message: 'Sipariş senkronizasyonu başarıyla tamamlandı',
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
            WooCommerce Sipariş Senkronizasyonu
          </Typography>

          <Box sx={{ my: 3 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Sipariş Durumu</InputLabel>
              <Select
                value={syncOptions.orderStatus}
                onChange={handleOrderStatusChange}
                label="Sipariş Durumu"
              >
                <MenuItem value="all">Tüm Siparişler</MenuItem>
                <MenuItem value="pending">Bekleyen Siparişler</MenuItem>
                <MenuItem value="processing">İşleme Alınan Siparişler</MenuItem>
                <MenuItem value="completed">Tamamlanan Siparişler</MenuItem>
                <MenuItem value="cancelled">İptal Edilen Siparişler</MenuItem>
                <MenuItem value="refunded">İade Edilen Siparişler</MenuItem>
              </Select>
            </FormControl>

            <TextField
              fullWidth
              type="date"
              label="Başlangıç Tarihi"
              name="startDate"
              value={syncOptions.dateRange.startDate}
              onChange={handleDateChange}
              sx={{ mb: 2 }}
              InputLabelProps={{ shrink: true }}
            />

            <TextField
              fullWidth
              type="date"
              label="Bitiş Tarihi"
              name="endDate"
              value={syncOptions.dateRange.endDate}
              onChange={handleDateChange}
              sx={{ mb: 2 }}
              InputLabelProps={{ shrink: true }}
            />

            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncCustomerData}
                  onChange={handleCheckboxChange}
                  name="syncCustomerData"
                />
              }
              label="Müşteri Bilgilerini Senkronize Et"
            />

            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.syncShippingDetails}
                  onChange={handleCheckboxChange}
                  name="syncShippingDetails"
                />
              }
              label="Kargo Bilgilerini Senkronize Et"
            />

            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.autoUpdateStatus}
                  onChange={handleCheckboxChange}
                  name="autoUpdateStatus"
                />
              }
              label="Sipariş Durumlarını Otomatik Güncelle"
            />

            <FormControlLabel
              control={
                <Checkbox
                  checked={syncOptions.notifyCustomers}
                  onChange={handleCheckboxChange}
                  name="notifyCustomers"
                />
              }
              label="Müşterilere Bildirim Gönder"
            />
          </Box>

          <Box sx={{ my: 3 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleStartSync}
              disabled={syncStatus.isRunning}
            >
              Sipariş Senkronizasyonunu Başlat
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

export default OrderSync; 