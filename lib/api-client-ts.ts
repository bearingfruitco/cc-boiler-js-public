export class ApiError extends Error {
  constructor(
    public status: number, 
    message: string, 
    public code?: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

interface ApiClientOptions extends RequestInit {
  params?: Record<string, string>;
  timeout?: number;
}

export async function apiClient<T = any>(
  endpoint: string,
  options?: ApiClientOptions
): Promise<T> {
  const { params, timeout = 30000, ...fetchOptions } = options || {};
  
  // Build URL with params
  const url = new URL(endpoint, window.location.origin);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
  }
  
  // Create abort controller for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url.toString(), {
      ...fetchOptions,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
    });
    
    clearTimeout(timeoutId);
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new ApiError(
        response.status,
        data.error || data.message || 'Request failed',
        data.code,
        data.details
      );
    }
    
    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (error instanceof ApiError) {
      throw error;
    }
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        throw new ApiError(408, 'Request timeout');
      }
      throw new ApiError(500, error.message);
    }
    
    throw new ApiError(500, 'Network error');
  }
}

// Convenience methods
export const api = {
  get: <T = any>(endpoint: string, options?: Omit<ApiClientOptions, 'method'>) => 
    apiClient<T>(endpoint, { ...options, method: 'GET' }),
    
  post: <T = any>(endpoint: string, data?: any, options?: Omit<ApiClientOptions, 'method' | 'body'>) => 
    apiClient<T>(endpoint, { ...options, method: 'POST', body: JSON.stringify(data) }),
    
  put: <T = any>(endpoint: string, data?: any, options?: Omit<ApiClientOptions, 'method' | 'body'>) => 
    apiClient<T>(endpoint, { ...options, method: 'PUT', body: JSON.stringify(data) }),
    
  patch: <T = any>(endpoint: string, data?: any, options?: Omit<ApiClientOptions, 'method' | 'body'>) => 
    apiClient<T>(endpoint, { ...options, method: 'PATCH', body: JSON.stringify(data) }),
    
  delete: <T = any>(endpoint: string, options?: Omit<ApiClientOptions, 'method'>) => 
    apiClient<T>(endpoint, { ...options, method: 'DELETE' }),
};
