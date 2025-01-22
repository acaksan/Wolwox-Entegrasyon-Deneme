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
  TextField
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
    }
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

  const handleStartSync = async () => {
    try {
      setSyncStatus({
        isRunning: true,
        progress: 0,
        message: 'Sipariş senkronizasyonu başlatılıyor...',
        logs: []
      });

      // API'ye senkronizasyon başlatma isteği gönder
      const response = await fetch('/api/wolvox/sync-orders', {
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
            Sipariş Senkronizasyonu
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