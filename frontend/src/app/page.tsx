'use client';

import { Box, Container, Typography } from '@mui/material';

export default function Home() {
  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          my: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Wolvox - WooCommerce Entegrasyonu
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Wolvox ERP ve WooCommerce arasında veri senkronizasyonu
        </Typography>
      </Box>
    </Container>
  );
} 