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
        <Typography variant="h2" component="h1" gutterBottom>
          Wolvox Entegrasyon
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          WooCommerce entegrasyonu ile ürünlerinizi kolayca yönetin
        </Typography>
      </Box>
    </Container>
  );
} 