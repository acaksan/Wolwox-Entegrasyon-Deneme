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

function WooCommerceSettings() {
  const [settings, setSettings] = useState({
    siteUrl: '',
    consumerKey: '',
    consumerSecret: '',
    version: 'wc/v3'
  });

  const [testResult, setTestResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTestConnection = async () => {
    try {
      const response = await fetch('/api/woocommerce/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
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
      const response = await fetch('/api/woocommerce/save-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
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
            WooCommerce API Ayarları
          </Typography>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Site URL"
                name="siteUrl"
                value={settings.siteUrl}
                onChange={handleChange}
                margin="normal"
                helperText="Örnek: https://www.siteniz.com"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Consumer Key"
                name="consumerKey"
                value={settings.consumerKey}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Consumer Secret"
                name="consumerSecret"
                type="password"
                value={settings.consumerSecret}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="API Versiyonu"
                name="version"
                value={settings.version}
                onChange={handleChange}
                margin="normal"
                disabled
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

export default WooCommerceSettings; 