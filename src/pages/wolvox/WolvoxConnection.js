import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Grid
} from '@mui/material';

function WolvoxConnection() {
  const [connectionSettings, setConnectionSettings] = useState({
    host: 'localhost',
    port: '3050',
    database: '',
    username: 'SYSDBA',
    password: 'masterkey',
    charset: 'UTF8'
  });

  const [testResult, setTestResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConnectionSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTestConnection = async () => {
    try {
      // API'ye bağlantı test isteği gönder
      const response = await fetch('/api/wolvox/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(connectionSettings),
      });

      const data = await response.json();

      if (response.ok) {
        setTestResult({
          success: true,
          message: 'Bağlantı başarılı!'
        });
      } else {
        setTestResult({
          success: false,
          message: data.message || 'Bağlantı hatası!'
        });
      }
    } catch (error) {
      setTestResult({
        success: false,
        message: 'Bağlantı testi sırasında bir hata oluştu.'
      });
    }
  };

  const handleSave = async () => {
    try {
      const response = await fetch('/api/wolvox/save-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(connectionSettings),
      });

      const data = await response.json();

      if (response.ok) {
        setTestResult({
          success: true,
          message: 'Ayarlar başarıyla kaydedildi!'
        });
      } else {
        setTestResult({
          success: false,
          message: data.message || 'Ayarlar kaydedilirken bir hata oluştu!'
        });
      }
    } catch (error) {
      setTestResult({
        success: false,
        message: 'Ayarlar kaydedilirken bir hata oluştu.'
      });
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Akınsoft Wolvox Firebird Bağlantı Ayarları
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Sunucu Adresi"
                name="host"
                value={connectionSettings.host}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Port"
                name="port"
                value={connectionSettings.port}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Veritabanı Yolu"
                name="database"
                value={connectionSettings.database}
                onChange={handleChange}
                margin="normal"
                helperText="Örnek: C:\Program Files\Wolvox2\Database\WOLVOX.FDB"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Kullanıcı Adı"
                name="username"
                value={connectionSettings.username}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Şifre"
                name="password"
                type="password"
                value={connectionSettings.password}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Karakter Seti"
                name="charset"
                value={connectionSettings.charset}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
          </Grid>

          {testResult && (
            <Alert 
              severity={testResult.success ? "success" : "error"}
              sx={{ mt: 2 }}
            >
              {testResult.message}
            </Alert>
          )}

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleTestConnection}
            >
              Bağlantıyı Test Et
            </Button>
            <Button
              variant="contained"
              color="success"
              onClick={handleSave}
            >
              Ayarları Kaydet
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}

export default WolvoxConnection; 