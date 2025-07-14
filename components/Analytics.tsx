'use client';

import { useEffect } from 'react';
import Script from 'next/script';

export function Analytics() {
  useEffect(() => {
    // Any client-side analytics initialization
    console.log('Analytics initialized');
  }, []);

  return (
    <>
      {/* Google Analytics */}
      {process.env.NEXT_PUBLIC_GA_ID && (
        <>
          <Script
            src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
            strategy="afterInteractive"
          />
          <Script id="google-analytics" strategy="afterInteractive">
            {`
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
            `}
          </Script>
        </>
      )}
      
      {/* Vercel Analytics */}
      {process.env.NODE_ENV === 'production' && (
        <Script
          src="https://va.vercel-scripts.com/v1/analytics/script.debug.js"
          strategy="afterInteractive"
        />
      )}
    </>
  );
}
