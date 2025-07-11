// hooks/mutations/index.ts
// SWR mutation hooks for data updates

import useSWRMutation from 'swr/mutation';
import { mutate } from 'swr';
import { useLeadStore } from '@/stores/lead-store';
import { useAnalyticsStore } from '@/stores/analytics-store';

// Types
interface CreateLeadData {
  name: string;
  email: string;
  phone: string;
  debt_amount: number;
  state: string;
  debt_types?: string[];
  credit_score?: string;
  monthly_income?: number;
  attribution?: Record<string, any>;
  interactions?: Record<string, any>;
}

interface UpdateLeadData {
  status?: 'contacted' | 'qualified' | 'converted' | 'rejected';
  qualification_status?: 'qualified' | 'not_qualified' | 'needs_review';
  partner_id?: string;
  notes?: string;
}

interface APIError {
  message: string;
  errors?: Record<string, string[]>;
  status: number;
}

// Fetcher functions
async function createLead(url: string, { arg }: { arg: CreateLeadData }) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to create lead');
  }
  
  return response.json();
}

async function updateLead(
  url: string,
  { arg }: { arg: { id: string; data: UpdateLeadData } }
) {
  const response = await fetch(`/api/leads/${arg.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg.data),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to update lead');
  }
  
  return response.json();
}

async function deleteLead(url: string, { arg }: { arg: { id: string } }) {
  const response = await fetch(`/api/leads/${arg.id}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to delete lead');
  }
  
  return response.json();
}

async function submitQuizResults(
  url: string,
  { arg }: { arg: { leadId: string; quizData: any } }
) {
  const response = await fetch(`/api/leads/${arg.leadId}/quiz`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg.quizData),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to submit quiz results');
  }
  
  return response.json();
}

// =================
// Lead Mutations
// =================

export function useCreateLead() {
  const { track } = useAnalyticsStore();
  const { formData, attribution, interactions } = useLeadStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/leads',
    createLead,
    {
      onSuccess: (data) => {
        // Track conversion
        track('Lead Created', {
          lead_id: data.id,
          debt_amount: data.debt_amount,
          qualification_status: data.qualification_status,
        });
        
        // Clear lead form
        useLeadStore.getState().resetForm();
        
        // Invalidate leads list
        mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads'),
          undefined,
          { revalidate: true }
        );
      },
      onError: (err) => {
        track('Lead Creation Failed', {
          error: err.message,
        });
      },
    }
  );
  
  const createLeadWithStoreData = async (additionalData?: Partial<CreateLeadData>) => {
    const leadData: CreateLeadData = {
      name: formData.name!,
      email: formData.email!,
      phone: formData.phone!,
      debt_amount: formData.debtAmount!,
      state: formData.state!,
      debt_types: formData.debtTypes,
      credit_score: formData.creditScore,
      monthly_income: formData.monthlyIncome,
      attribution,
      interactions: {
        ...interactions,
        total_time_spent: Date.now() - interactions.started_at,
      },
      ...additionalData,
    };
    
    return trigger(leadData);
  };
  
  return {
    createLead: trigger,
    createLeadWithStoreData,
    isCreating: isMutating,
    error,
  };
}

export function useUpdateLead() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/leads',
    updateLead,
    {
      onSuccess: async (data, variables) => {
        // Track update
        track('Lead Updated', {
          lead_id: variables.arg.id,
          updated_fields: Object.keys(variables.arg.data),
        });
        
        // Update specific lead in cache
        await mutate(`/api/leads/${variables.arg.id}`, data, false);
        
        // Revalidate lists
        await mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads?'),
          undefined,
          { revalidate: true }
        );
      },
      optimisticData: (current, variables) => {
        // Optimistically update the UI
        if (!current) return current;
        return { ...current, ...variables.arg.data };
      },
      rollbackOnError: true,
    }
  );
  
  return {
    updateLead: trigger,
    isUpdating: isMutating,
    error,
  };
}

export function useDeleteLead() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/leads',
    deleteLead,
    {
      onSuccess: async (_, variables) => {
        // Track deletion
        track('Lead Deleted', {
          lead_id: variables.arg.id,
        });
        
        // Remove from cache
        await mutate(`/api/leads/${variables.arg.id}`, undefined, false);
        
        // Revalidate lists
        await mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads'),
          undefined,
          { revalidate: true }
        );
      },
    }
  );
  
  return {
    deleteLead: trigger,
    isDeleting: isMutating,
    error,
  };
}

// =================
// Quiz Mutations
// =================

export function useSubmitQuizResults() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/quiz/submit',
    submitQuizResults,
    {
      onSuccess: (data, variables) => {
        // Track quiz submission
        track('Quiz Results Submitted', {
          lead_id: variables.arg.leadId,
          qualification_status: data.qualification_status,
        });
        
        // Update lead in cache with quiz results
        mutate(
          `/api/leads/${variables.arg.leadId}`,
          async (currentLead: any) => ({
            ...currentLead,
            quiz_completed: true,
            qualification_status: data.qualification_status,
            quiz_results: data.quiz_results,
          }),
          false
        );
      },
    }
  );
  
  return {
    submitQuizResults: trigger,
    isSubmitting: isMutating,
    error,
  };
}

// =================
// Partner Mutations
// =================

async function acceptLead(
  url: string,
  { arg }: { arg: { leadId: string; partnerId: string; notes?: string } }
) {
  const response = await fetch(`/api/partners/${arg.partnerId}/leads/${arg.leadId}/accept`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ notes: arg.notes }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to accept lead');
  }
  
  return response.json();
}

async function rejectLead(
  url: string,
  { arg }: { arg: { leadId: string; partnerId: string; reason: string } }
) {
  const response = await fetch(`/api/partners/${arg.partnerId}/leads/${arg.leadId}/reject`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ reason: arg.reason }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to reject lead');
  }
  
  return response.json();
}

export function useAcceptLead() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/partners/leads/accept',
    acceptLead,
    {
      onSuccess: (data, variables) => {
        // Track acceptance
        track('Lead Accepted', {
          lead_id: variables.arg.leadId,
          partner_id: variables.arg.partnerId,
        });
        
        // Update lead status
        mutate(`/api/leads/${variables.arg.leadId}`);
        
        // Revalidate partner performance
        mutate(`/api/partners/${variables.arg.partnerId}/performance`);
      },
    }
  );
  
  return {
    acceptLead: trigger,
    isAccepting: isMutating,
    error,
  };
}

export function useRejectLead() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/partners/leads/reject',
    rejectLead,
    {
      onSuccess: (data, variables) => {
        // Track rejection
        track('Lead Rejected', {
          lead_id: variables.arg.leadId,
          partner_id: variables.arg.partnerId,
          reason: variables.arg.reason,
        });
        
        // Update lead status
        mutate(`/api/leads/${variables.arg.leadId}`);
      },
    }
  );
  
  return {
    rejectLead: trigger,
    isRejecting: isMutating,
    error,
  };
}

// =================
// Bulk Operations
// =================

async function bulkUpdateLeads(
  url: string,
  { arg }: { arg: { leadIds: string[]; updates: UpdateLeadData } }
) {
  const response = await fetch('/api/leads/bulk', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      lead_ids: arg.leadIds,
      updates: arg.updates,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to update leads');
  }
  
  return response.json();
}

export function useBulkUpdateLeads() {
  const { track } = useAnalyticsStore();
  
  const { trigger, isMutating, error } = useSWRMutation(
    '/api/leads/bulk',
    bulkUpdateLeads,
    {
      onSuccess: (data, variables) => {
        // Track bulk update
        track('Leads Bulk Updated', {
          count: variables.arg.leadIds.length,
          updated_fields: Object.keys(variables.arg.updates),
        });
        
        // Invalidate all affected leads
        variables.arg.leadIds.forEach(leadId => {
          mutate(`/api/leads/${leadId}`);
        });
        
        // Revalidate lists
        mutate(
          (key) => typeof key === 'string' && key.startsWith('/api/leads'),
          undefined,
          { revalidate: true }
        );
      },
    }
  );
  
  return {
    bulkUpdateLeads: trigger,
    isUpdating: isMutating,
    error,
  };
}

// =================
// Form Draft Mutations
// =================

async function saveDraft(
  url: string,
  { arg }: { arg: { formData: any; attribution: any } }
) {
  const response = await fetch('/api/leads/draft', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to save draft');
  }
  
  return response.json();
}

export function useSaveDraft() {
  const { formData, attribution } = useLeadStore();
  
  const { trigger, isMutating } = useSWRMutation(
    '/api/leads/draft',
    saveDraft,
    {
      onSuccess: (data) => {
        console.log('Draft saved:', data.id);
      },
      onError: (err) => {
        console.error('Failed to save draft:', err);
      },
    }
  );
  
  const saveDraftWithStoreData = () => {
    return trigger({ formData, attribution });
  };
  
  return {
    saveDraft: trigger,
    saveDraftWithStoreData,
    isSaving: isMutating,
  };
}

// =================
// Analytics Mutations
// =================

async function trackEvent(
  url: string,
  { arg }: { arg: { event: string; properties: any } }
) {
  const response = await fetch('/api/analytics/track', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(arg),
  });
  
  if (!response.ok) {
    throw new Error('Failed to track event');
  }
  
  return response.json();
}

export function useTrackEvent() {
  const { trigger } = useSWRMutation(
    '/api/analytics/track',
    trackEvent,
    {
      // Fire and forget - don't wait for response
      populateCache: false,
      revalidate: false,
    }
  );
  
  return {
    trackEvent: trigger,
  };
}

// =================
// Error Handling Helper
// =================

export function useHandleMutationError() {
  const { track } = useAnalyticsStore();
  
  const handleError = (error: any, context: string) => {
    // Track error
    track('API Error', {
      context,
      error_message: error.message,
      error_status: error.status,
    });
    
    // Parse error for user display
    if (error.info?.errors) {
      // Validation errors
      const messages = Object.entries(error.info.errors)
        .map(([field, errors]) => `${field}: ${(errors as string[]).join(', ')}`)
        .join('\n');
      return messages;
    }
    
    // Generic error message
    return error.message || 'An unexpected error occurred';
  };
  
  return { handleError };
}