import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api/client';
import { queryKeys } from '@/lib/query/client';

export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export function useUser(userId?: string) {
  return useQuery({
    queryKey: queryKeys.user(userId!),
    queryFn: () => apiClient<User>(`/users/${userId}`),
    enabled: !!userId,
  });
}

export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: () => apiClient<User>('/auth/me'),
    staleTime: 5 * 60 * 1000, // Consider current user data fresh for 5 minutes
  });
}
