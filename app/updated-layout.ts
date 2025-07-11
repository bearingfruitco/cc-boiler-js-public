// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import { Analytics } from '@/components/Analytics';
import './globals.css';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'FreshSlate - Get Out of Debt',
  description: 'Find the right debt relief solution for your situation',
  keywords: 'debt relief, debt settlement, credit counseling, debt consolidation',
  openGraph: {
    title: 'FreshSlate - Get Out of Debt',
    description: 'Find the right debt relief solution for your situation',
    type: 'website',
    url: 'https://freshslate.com',
    images: [
      {
        url: 'https://freshslate.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'FreshSlate - Debt Relief Solutions',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'FreshSlate - Get Out of Debt',
    description: 'Find the right debt relief solution for your situation',
    images: ['https://freshslate.com/og-image.png'],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <head>
        {/* Preconnect to external domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://cdn.rudderlabs.com" />
        
        {/* Favicon */}
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        
        {/* Theme color */}
        <meta name="theme-color" content="#2563eb" />
      </head>
      <body className="font-sans antialiased">
        <Providers>
          {children}
        </Providers>
        <Analytics />
      </body>
    </html>
  );
}