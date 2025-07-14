// hooks/queries/index.ts
// SWR query hooks for data fetching

import useSWR, { SWRConfiguration } from 'swr';
import useSWRInfinite from 'swr/infinite';

// Types
interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  debt_amount: number;
  state: string;
  status: 'new' | 'contacted' | 'qualified' | 'converted' | 'rejected';
  created_at: string;
  updated_at: string;
  qualification_status?: 'qualified' | 'not_qualified' | 'needs_review';
  partner_matched?: boolean;
  attribution?: Record<string, any>;
}

interface LeadStats {
  total_leads: number;
  qualified_leads: number;
  conversion_rate: number;
  average_debt_amount: number;
  leads_by_state: Record<string, number>;
  leads_by_source: Record<string, number>;
  daily_leads: Array<{ date: string; count: number }>;
}

interface Partner {
  id: string;
  name: string;
  type: 'settlement' | 'consolidation' | 'counseling';
  states_licensed: string[];
  min_debt_amount: number;
  max_debt_amount: number;
  acceptance_rate: number;
  response_time_avg: number;
  active: boolean;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

// Default SWR configuration
const defaultConfig: SWRConfiguration = {
  revalidateOnFocus: false,
  revalidateOnReconnect: true,
  dedupingInterval: 2000,
};

// Fetcher function
const fetcher = async (url: string) => {
  const res = await fetch(url);
  
  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    (error as any).info = await res.json();
    (error as any).status = res.status;
    throw error;
  }
  
  return res.json();
};

// =================
// Lead Queries
// =================

export function useLeads(filters?: {
  page?: number;
  status?: Lead['status'];
  state?: string;
  dateFrom?: string;
  dateTo?: string;
  search?: string;
}) {
  const params = new URLSearchParams();
  
  if (filters?.page) params.append('page', filters.page.toString());
  if (filters?.status) params.append('status', filters.status);
  if (filters?.state) params.append('state', filters.state);
  if (filters?.dateFrom) params.append('date_from', filters.dateFrom);
  if (filters?.dateTo) params.append('date_to', filters.dateTo);
  if (filters?.search) params.append('search', filters.search);
  
  const { data, error, isLoading, isValidating, mutate } = useSWR<PaginatedResponse<Lead>>(
    `/api/leads?${params.toString()}`,
    fetcher,
    {
      ...defaultConfig,
      refreshInterval: 30000, // Refresh every 30 seconds
    }
  );
  
  return {
    leads: data?.data ?? [],
    meta: data?.meta,
    isLoading,
    isValidating,
    isError: error,
    mutate,
    refresh: () => mutate(),
  };
}

export function useLeadById(leadId: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Lead>(
    leadId ? `/api/leads/${leadId}` : null,
    fetcher,
    defaultConfig
  );
  
  return {
    lead: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useLeadStats(dateRange?: { from: string; to: string }) {
  const params = new URLSearchParams();
  if (dateRange?.from) params.append('from', dateRange.from);
  if (dateRange?.to) params.append('to', dateRange.to);
  
  const { data, error, isLoading } = useSWR<LeadStats>(
    `/api/stats/leads?${params.toString()}`,
    fetcher,
    {
      ...defaultConfig,
      refreshInterval: 60000, // Refresh every minute
    }
  );
  
  return {
    stats: data,
    isLoading,
    isError: error,
  };
}

// Infinite scroll for leads
export function useInfiniteLeads(filters?: {
  status?: Lead['status'];
  state?: string;
}) {
  const getKey = (pageIndex: number, previousPageData: PaginatedResponse<Lead> | null) => {
    if (previousPageData && !previousPageData.data.length) return null;
    
    const params = new URLSearchParams();
    params.append('page', (pageIndex + 1).toString());
    params.append('per_page', '20');
    
    if (filters?.status) params.append('status', filters.status);
    if (filters?.state) params.append('state', filters.state);
    
    return `/api/leads?${params.toString()}`;
  };
  
  const { data, error, size, setSize, isValidating, isLoading, mutate } = useSWRInfinite<PaginatedResponse<Lead>>(
    getKey,
    fetcher,
    {
      ...defaultConfig,
      revalidateFirstPage: false,
      revalidateAll: false,
    }
  );
  
  const leads = data ? data.flatMap(page => page.data) : [];
  const isLoadingMore = isLoading || (size > 0 && data && typeof data[size - 1] === 'undefined');
  const isEmpty = data?.[0]?.data.length === 0;
  const isReachingEnd = isEmpty || (data && data[data.length - 1]?.data.length < 20);
  
  return {
    leads,
    error,
    isLoading,
    isLoadingMore,
    isReachingEnd,
    isEmpty,
    size,
    setSize,
    mutate,
    loadMore: () => setSize(size + 1),
  };
}

// =================
// Partner Queries
// =================

export function usePartners(filters?: {
  active?: boolean;
  type?: Partner['type'];
  state?: string;
}) {
  const params = new URLSearchParams();
  
  if (filters?.active !== undefined) params.append('active', filters.active.toString());
  if (filters?.type) params.append('type', filters.type);
  if (filters?.state) params.append('state', filters.state);
  
  const { data, error, isLoading, mutate } = useSWR<Partner[]>(
    `/api/partners?${params.toString()}`,
    fetcher,
    defaultConfig
  );
  
  return {
    partners: data ?? [],
    isLoading,
    isError: error,
    mutate,
  };
}

export function usePartnerById(partnerId: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Partner>(
    partnerId ? `/api/partners/${partnerId}` : null,
    fetcher,
    defaultConfig
  );
  
  return {
    partner: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function usePartnerPerformance(partnerId: string, dateRange?: { from: string; to: string }) {
  const params = new URLSearchParams();
  if (dateRange?.from) params.append('from', dateRange.from);
  if (dateRange?.to) params.append('to', dateRange.to);
  
  const { data, error, isLoading } = useSWR(
    `/api/partners/${partnerId}/performance?${params.toString()}`,
    fetcher,
    {
      ...defaultConfig,
      refreshInterval: 300000, // Refresh every 5 minutes
    }
  );
  
  return {
    performance: data,
    isLoading,
    isError: error,
  };
}

// =================
// Dashboard Queries
// =================

export function useDashboardStats() {
  const { data, error, isLoading } = useSWR(
    '/api/dashboard/stats',
    fetcher,
    {
      ...defaultConfig,
      refreshInterval: 30000, // Refresh every 30 seconds
    }
  );
  
  return {
    stats: data,
    isLoading,
    isError: error,
  };
}

export function useRecentActivity(limit = 10) {
  const { data, error, isLoading } = useSWR(
    `/api/dashboard/activity?limit=${limit}`,
    fetcher,
    {
      ...defaultConfig,
      refreshInterval: 10000, // Refresh every 10 seconds
    }
  );
  
  return {
    activities: data ?? [],
    isLoading,
    isError: error,
  };
}

// =================
// Analytics Queries
// =================

export function useConversionFunnel(dateRange?: { from: string; to: string }) {
  const params = new URLSearchParams();
  if (dateRange?.from) params.append('from', dateRange.from);
  if (dateRange?.to) params.append('to', dateRange.to);
  
  const { data, error, isLoading } = useSWR(
    `/api/analytics/funnel?${params.toString()}`,
    fetcher,
    defaultConfig
  );
  
  return {
    funnel: data,
    isLoading,
    isError: error,
  };
}

export function useAttributionReport(dateRange?: { from: string; to: string }) {
  const params = new URLSearchParams();
  if (dateRange?.from) params.append('from', dateRange.from);
  if (dateRange?.to) params.append('to', dateRange.to);
  
  const { data, error, isLoading } = useSWR(
    `/api/analytics/attribution?${params.toString()}`,
    fetcher,
    defaultConfig
  );
  
  return {
    attribution: data,
    isLoading,
    isError: error,
  };
}

// =================
// Utility Hooks
// =================

// Prefetch data for faster navigation
export function usePrefetch() {
  const prefetchLeadById = (leadId: string) => {
    mutate(
      `/api/leads/${leadId}`,
      fetch(`/api/leads/${leadId}`).then(res => res.json()),
      { revalidate: false }
    );
  };
  
  const prefetchPartnerById = (partnerId: string) => {
    mutate(
      `/api/partners/${partnerId}`,
      fetch(`/api/partners/${partnerId}`).then(res => res.json()),
      { revalidate: false }
    );
  };
  
  return {
    prefetchLeadById,
    prefetchPartnerById,
  };
}

// Clear all SWR cache
export function useClearCache() {
  const clearCache = () => {
    mutate(() => true, undefined, { revalidate: false });
  };
  
  return { clearCache };
}

// Export mutate for external use
export { mutate } from 'swr';