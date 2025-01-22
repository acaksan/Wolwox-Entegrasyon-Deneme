import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Button,
  Typography,
  Alert,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  TextField
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import trLocale from 'date-fns/locale/tr';

const OrderSync = () => {
  const [syncStatus, setSyncStatus] = useState({
    isRunning: false,
    progress: 0,
    message: '',
    success: null
  });

  const [syncOptions, setSyncOptions] = useState({
    startDate: new Date(new Date().setDate(new Date().getDate() - 30)), // Son 30 gün
    endDate: new Date(),
    orderStatus: 'all'
  });

  const handleDateChange = (field) => (date) => {
    setSyncOptions({
      ...syncOptions,
      [field]: date
    });
  };

  const handleStatusChange = (event) => {
    setSyncOptions({
      ...syncOptions,
      orderStatus: event.target.value
    });
  };

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'Sipariş senkronizasyonu başlatılıyor...',
        success: null
      });

      const response = await fetch('/api/woocommerce/orders/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          startDate: syncOptions.startDate.toISOString(),
          endDate: syncOptions.endDate.toISOString(),
          status: syncOptions.orderStatus
        })
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
            WooCommerce Sipariş Senkronizasyonu
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={trLocale}>
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="Başlangıç Tarihi"
                  value={syncOptions.startDate}
                  onChange={handleDateChange('startDate')}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="Bitiş Tarihi"
                  value={syncOptions.endDate}
                  onChange={handleDateChange('endDate')}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
            </LocalizationProvider>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Sipariş Durumu</InputLabel>
                <Select
                  value={syncOptions.orderStatus}
                  onChange={handleStatusChange}
                  label="Sipariş Durumu"
                >
                  <MenuItem value="all">Tümü</MenuItem>
                  <MenuItem value="processing">İşlemde</MenuItem>
                  <MenuItem value="completed">Tamamlandı</MenuItem>
                  <MenuItem value="on-hold">Beklemede</MenuItem>
                  <MenuItem value="cancelled">İptal Edildi</MenuItem>
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

export default OrderSync; 