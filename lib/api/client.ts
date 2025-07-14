// API client for making HTTP requests

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiClient<T = any>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`/api${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new ApiError(response.status, message || 'Request failed');
  }

  return response.json();
}

// Helper functions
export const api = {
  get: <T = any>(endpoint: string) => 
    apiClient<T>(endpoint, { method: 'GET' }),
    
  post: <T = any>(endpoint: string, data: any) => 
    apiClient<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    
  patch: <T = any>(endpoint: string, data: any) => 
    apiClient<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    
  delete: (endpoint: string) => 
    apiClient(endpoint, { method: 'DELETE' }),
};
