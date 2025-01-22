import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, Button, Grid, Card, CardContent, Alert } from '@mui/material';

const WolvoxConnection = () => {
  const [settings, setSettings] = useState({
    host: 'localhost',
    port: '3050',
    database: '',
    username: 'SYSDBA',
    password: 'masterkey',
    charset: 'WIN1254'
  });

  const [status, setStatus] = useState({
    loading: false,
    success: false,
    error: null,
    message: ''
  });

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const response = await fetch('/api/firebird/settings');
        
        // Content-Type kontrolü
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new Error('Sunucudan geçersiz yanıt alındı');
        }

        if (response.ok) {
          const data = await response.json();
          setSettings(data);
        } else {
          throw new Error('Ayarlar yüklenemedi');
        }
      } catch (error) {
        console.error('Ayarlar yüklenirken hata:', error);
        setStatus({
          loading: false,
          success: false,
          error: true,
          message: error.message
        });
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
      const response = await fetch('/api/firebird/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
      });

      // Content-Type kontrolü
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Sunucudan geçersiz yanıt alındı');
      }

      const data = await response.json();
      
      if (response.ok) {
        setStatus({
          loading: false,
          success: true,
          error: null,
          message: 'Ayarlar başarıyla kaydedildi'
        });
      } else {
        throw new Error(data.message || 'Ayarlar kaydedilemedi');
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
      const response = await fetch('/api/firebird/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
      });

      // Content-Type kontrolü
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Sunucudan geçersiz yanıt alındı');
      }

      const data = await response.json();
      
      if (response.ok && data.success) {
        setStatus({
          loading: false,
          success: true,
          error: null,
          message: 'Bağlantı testi başarılı'
        });
      } else {
        throw new Error(data.message || 'Bağlantı testi başarısız');
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
        Akınsoft Wolvox Bağlantı Ayarları
      </Typography>
      
      <Card>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Sunucu"
                name="host"
                value={settings.host}
                onChange={handleChange}
                helperText="Örnek: localhost veya IP adresi"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Port"
                name="port"
                value={settings.port}
                onChange={handleChange}
                helperText="Varsayılan: 3050"
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Veritabanı Yolu"
                name="database"
                value={settings.database}
                onChange={handleChange}
                helperText="Örnek: D:\AKINSOFT\Wolvox8\Database_FB\WOLVOX.FDB"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Kullanıcı Adı"
                name="username"
                value={settings.username}
                onChange={handleChange}
                helperText="Varsayılan: SYSDBA"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Şifre"
                name="password"
                value={settings.password}
                onChange={handleChange}
                type="password"
                helperText="Varsayılan: masterkey"
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Karakter Seti"
                name="charset"
                value={settings.charset}
                onChange={handleChange}
                helperText="Varsayılan: WIN1254"
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

export default WolvoxConnection; 