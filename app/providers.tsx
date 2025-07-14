'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState, useEffect } from 'react';
import { initializeApp } from '@/lib/analytics';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Stale time of 60 seconds
            staleTime: 60 * 1000,
            // Cache time of 5 minutes
            gcTime: 5 * 60 * 1000,
            // Retry failed requests 3 times
            retry: 3,
            // Retry delay exponential backoff
            retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
            // Refetch on window focus
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  // Initialize analytics and event system
  useEffect(() => {
    initializeApp();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
