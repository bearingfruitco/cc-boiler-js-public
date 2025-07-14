/** @type {import('next').NextConfig} */
const nextConfig = {
  // React 19 and Next.js 15 configuration
  reactStrictMode: true,
  
  // Experimental features for Next.js 15
  experimental: {
    // Enable typed routes
    typedRoutes: true,
    // Server actions configuration
    serverActions: {
      bodySizeLimit: '2mb',
      allowedOrigins: ['localhost:3000'],
    },
  },
  
  // Image optimization with sharp
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.supabase.co',
        pathname: '/storage/v1/object/public/**',
      },
      {
        protocol: 'https',
        hostname: '**.githubusercontent.com',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Performance optimizations
  poweredByHeader: false,
  compress: true,
  
  // Webpack configuration for bundle analyzer
  webpack: (config, { isServer, dev }) => {
    // Bundle analyzer setup
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer
            ? '../analyze/server.html'
            : '../analyze/client.html',
          openAnalyzer: false,
        })
      );
    }
    
    // Tailwind v4 doesn't need special webpack config
    return config;
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()',
          },
        ],
      },
    ];
  },
  
  // Redirects
  async redirects() {
    return [
      // Add any redirects here
    ];
  },
  
  // Environment variables to expose to the browser
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.npm_package_version || '1.0.0',
  },
};

// Sentry wrapper for error monitoring
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = process.env.NODE_ENV === 'production' 
  ? withSentryConfig(
      nextConfig,
      {
        silent: true,
        org: process.env.SENTRY_ORG,
        project: process.env.SENTRY_PROJECT,
      },
      {
        widenClientFileUpload: true,
        transpileClientSDK: true,
        tunnelRoute: '/monitoring',
        hideSourceMaps: true,
        disableLogger: true,
      }
    )
  : nextConfig;
