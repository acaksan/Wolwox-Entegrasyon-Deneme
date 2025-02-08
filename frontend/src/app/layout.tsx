import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ThemeRegistry from '@/components/ThemeRegistry/ThemeRegistry';
import { Provider } from 'react-redux';
import { store } from '@/store';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Wolvox - WooCommerce Entegrasyonu',
  description: 'Wolvox ERP ve WooCommerce entegrasyon uygulaması',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <body className={inter.className}>
        <Provider store={store}>
          <ThemeRegistry>{children}</ThemeRegistry>
        </Provider>
      </body>
    </html>
  );
} 