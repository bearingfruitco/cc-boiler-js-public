// app/providers.tsx
'use client';

import { SWRConfig } from 'swr';
import { ReactNode } from 'react';

// Default fetcher function
const fetcher = async (url: string) => {
  const res = await fetch(url);
  
  // If the status code is not in the range 200-299,
  // we still try to parse and throw it.
  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    // Attach extra info to the error object.
    (error as any).info = await res.json();
    (error as any).status = res.status;
    throw error;
  }
  
  return res.json();
};

// Global SWR configuration
const swrConfig = {
  fetcher,
  revalidateOnFocus: false, // Don't revalidate when window gets focus (good for forms)
  revalidateOnReconnect: true, // Revalidate when network reconnects
  refreshInterval: 0, // No automatic refresh by default
  dedupingInterval: 2000, // Dedupe requests within 2 seconds
  errorRetryCount: 3, // Retry failed requests 3 times
  errorRetryInterval: 5000, // Wait 5 seconds between retries
  shouldRetryOnError: (error: any) => {
    // Don't retry on 4xx errors (client errors)
    if (error?.status >= 400 && error?.status < 500) {
      return false;
    }
    return true;
  },
  onError: (error: any, key: string) => {
    // Global error handler
    if (error?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    
    // Log errors in development
    if (process.env.NODE_ENV === 'development') {
      console.error(`SWR Error for ${key}:`, error);
    }
  },
  onSuccess: (data: any, key: string) => {
    // Global success handler
    if (process.env.NODE_ENV === 'development') {
      console.log(`SWR Success for ${key}`);
    }
  },
};

interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <SWRConfig value={swrConfig}>
      {children}
    </SWRConfig>
  );
}