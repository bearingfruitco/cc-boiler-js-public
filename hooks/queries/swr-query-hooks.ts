// hooks/queries/swr-query-hooks.ts
import useSWR from 'swr';
import { mutate } from 'swr';

// Base fetcher
const fetcher = async (url: string) => {
  const response = await fetch(url);
  if (!response.ok) {
    const error = new Error('An error occurred while fetching the data.');
    (error as any).info = await response.json();
    (error as any).status = response.status;
    throw error;
  }
  return response.json();
};

// Lead queries
export function useLeads(params?: {
  status?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  limit?: number;
}) {
  const queryString = params ? '?' + new URLSearchParams(params as any).toString() : '';
  const { data, error, isLoading } = useSWR(
    `/api/leads${queryString}`,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
    }
  );

  return {
    leads: data?.leads || [],
    pagination: data?.pagination,
    isLoading,
    error,
  };
}

export function useLead(id: string) {
  const { data, error, isLoading } = useSWR(
    id ? `/api/leads/${id}` : null,
    fetcher
  );

  return {
    lead: data,
    isLoading,
    error,
  };
}

// Partner performance
export function usePartnerPerformance(partnerId?: string) {
  const { data, error, isLoading } = useSWR(
    partnerId ? `/api/partners/${partnerId}/performance` : null,
    fetcher,
    {
      refreshInterval: 60000, // Refresh every minute
    }
  );

  return {
    performance: data,
    isLoading,
    error,
  };
}

// Analytics queries
export function useAnalyticsSummary(timeframe: 'today' | 'week' | 'month' | 'all' = 'today') {
  const { data, error, isLoading } = useSWR(
    `/api/analytics/summary?timeframe=${timeframe}`,
    fetcher,
    {
      refreshInterval: 30000, // Refresh every 30 seconds
    }
  );

  return {
    summary: data,
    isLoading,
    error,
  };
}

// Session tracking
export function useSession() {
  const { data, error, isLoading } = useSWR(
    '/api/session',
    fetcher,
    {
      revalidateOnFocus: true,
      dedupingInterval: 10000,
    }
  );

  return {
    session: data,
    isLoading,
    error,
  };
}

// Field validation
export function useFieldValidation(field: string, value: any) {
  const { data, error } = useSWR(
    field && value ? `/api/validate/${field}?value=${encodeURIComponent(value)}` : null,
    fetcher,
    {
      dedupingInterval: 1000,
    }
  );

  return {
    isValid: data?.valid,
    validationError: data?.error,
    error,
  };
}

// Manual mutations (for complex cases)
export async function optimisticUpdateLead(leadId: string, updates: any) {
  // Optimistically update the cache
  await mutate(
    `/api/leads/${leadId}`,
    async (currentData: any) => ({ ...currentData, ...updates }),
    false
  );
  
  // Then send the request
  try {
    const response = await fetch(`/api/leads/${leadId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    
    if (!response.ok) throw new Error('Update failed');
    
    const updated = await response.json();
    
    // Revalidate with server data
    await mutate(`/api/leads/${leadId}`, updated);
    
    return updated;
  } catch (error) {
    // Revert on error
    await mutate(`/api/leads/${leadId}`);
    throw error;
  }
}

// Bulk operations
export async function bulkUpdateLeads(leadIds: string[], updates: any) {
  const promises = leadIds.map(id => optimisticUpdateLead(id, updates));
  return Promise.all(promises);
}

// Clear all caches
export function clearAllCaches() {
  // Clear specific cache patterns
  void mutate(() => true, undefined, { revalidate: false });
}

// Prefetch data
export async function prefetchLeads() {
  const data = await fetcher('/api/leads');
  void mutate('/api/leads', data);
  return data;
}

// Export mutate for external use
export { mutate };
