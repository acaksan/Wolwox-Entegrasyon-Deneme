import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Alert,
  Grid,
  Typography
} from '@mui/material';

const WooCommerceSettings = () => {
  const [settings, setSettings] = useState({
    url: '',
    key: '',
    secret: ''
  });

  const [status, setStatus] = useState({
    loading: false,
    success: false,
    error: null,
    message: ''
  });

  // Mevcut ayarları yükle
  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await fetch('/api/woocommerce/settings/current');
        if (response.ok) {
          const data = await response.json();
          setSettings(data);
        }
      } catch (error) {
        console.error('Ayarlar yüklenirken hata:', error);
      }
    };
    loadSettings();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    setStatus({ loading: true, success: false, error: null, message: '' });
    try {
      const response = await fetch('/api/woocommerce/settings/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
      });

      const data = await response.json();
      
      if (response.ok) {
        setStatus({
          loading: false,
          success: true,
          error: null,
          message: 'Ayarlar başarıyla kaydedildi'
        });
      } else {
        throw new Error(data.error || 'Ayarlar kaydedilemedi');
      }
    } catch (error) {
      setStatus({
        loading: false,
        success: false,
        error: true,
        message: error.message
      });
    }
  };

  const handleTest = async () => {
    setStatus({ loading: true, success: false, error: null, message: '' });
    try {
      const response = await fetch('/api/woocommerce/settings/test');
      const data = await response.json();
      
      if (response.ok && data.success) {
        setStatus({
          loading: false,
          success: true,
          error: null,
          message: 'Bağlantı testi başarılı'
        });
      } else {
        throw new Error(data.error || 'Bağlantı testi başarısız');
      }
    } catch (error) {
      setStatus({
        loading: false,
        success: false,
        error: true,
        message: error.message
      });
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        WooCommerce Bağlantı Ayarları
      </Typography>
      
      <Card>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Site URL"
                name="url"
                value={settings.url}
                onChange={handleChange}
                helperText="Örnek: https://www.siteniz.com"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Consumer Key"
                name="key"
                value={settings.key}
                onChange={handleChange}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Consumer Secret"
                name="secret"
                value={settings.secret}
                onChange={handleChange}
                type="password"
              />
            </Grid>

            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleSave}
                  disabled={status.loading}
                >
                  {status.loading ? 'Kaydediliyor...' : 'Kaydet'}
                </Button>
                
                <Button
                  variant="outlined"
                  onClick={handleTest}
                  disabled={status.loading}
                >
                  {status.loading ? 'Test Ediliyor...' : 'Bağlantıyı Test Et'}
                </Button>
              </Box>
            </Grid>

            {(status.success || status.error) && (
              <Grid item xs={12}>
                <Alert severity={status.error ? 'error' : 'success'}>
                  {status.message}
                </Alert>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default WooCommerceSettings; 