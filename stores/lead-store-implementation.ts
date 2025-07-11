// stores/lead-store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { devtools } from 'zustand/middleware';

interface LeadFormData {
  // Personal Information
  name?: string;
  email?: string;
  phone?: string;
  
  // Debt Information
  debtAmount?: number;
  debtTypes?: string[];
  monthlyPayment?: number;
  behindOnPayments?: boolean;
  
  // Financial Situation
  state?: string;
  creditScore?: string;
  monthlyIncome?: number;
  employmentStatus?: string;
  
  // Additional Info
  homeOwner?: boolean;
  filedBankruptcy?: boolean;
  bestTimeToCall?: string;
  agreeToTerms?: boolean;
}

interface Attribution {
  // UTM Parameters
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
  
  // Platform Click IDs
  gclid?: string;
  fbclid?: string;
  ttclid?: string;
  msclkid?: string;
  
  // Session Info
  landing_page?: string;
  referrer?: string;
  ip_address?: string;
  user_agent?: string;
  session_id?: string;
  
  // Timestamps
  first_visit?: string;
  page_views?: number;
}

interface InteractionTracking {
  started_at: number;
  last_interaction: number;
  field_touches: Record<string, number>;
  field_times: Record<string, number>;
  abandoned_fields: string[];
  validation_errors: Record<string, string[]>;
  total_time_spent: number;
  completion_percentage: number;
}

interface LeadState {
  // Form Data
  formData: LeadFormData;
  
  // Attribution
  attribution: Attribution;
  
  // Interaction Tracking
  interactions: InteractionTracking;
  
  // UI State
  currentStep: number;
  isSubmitting: boolean;
  submitError: string | null;
  
  // Actions
  updateField: (field: keyof LeadFormData, value: any) => void;
  updateMultipleFields: (fields: Partial<LeadFormData>) => void;
  setAttribution: (attribution: Partial<Attribution>) => void;
  trackFieldInteraction: (field: string) => void;
  trackFieldTime: (field: string, time: number) => void;
  trackValidationError: (field: string, error: string) => void;
  markFieldAbandoned: (field: string) => void;
  
  // Form Actions
  setCurrentStep: (step: number) => void;
  submitForm: () => Promise<{ success: boolean; leadId?: string; error?: string }>;
  resetForm: () => void;
  
  // Computed Values
  getCompletionPercentage: () => number;
  getRequiredFieldsStatus: () => Record<string, boolean>;
  isFormValid: () => boolean;
  getTimeSpentOnField: (field: string) => number;
  getTotalTimeSpent: () => number;
}

// Helper function to get required fields based on current data
function getRequiredFields(formData: LeadFormData): string[] {
  const baseFields = ['name', 'email', 'phone', 'debtAmount', 'state'];
  
  // Add conditional required fields
  if (formData.debtAmount && formData.debtAmount >= 10000) {
    baseFields.push('debtTypes', 'creditScore');
  }
  
  return baseFields;
}

// Create the store
export const useLeadStore = create<LeadState>()(
  devtools(
    persist(
      immer((set, get) => ({
        // Initial State
        formData: {},
        attribution: {},
        interactions: {
          started_at: Date.now(),
          last_interaction: Date.now(),
          field_touches: {},
          field_times: {},
          abandoned_fields: [],
          validation_errors: {},
          total_time_spent: 0,
          completion_percentage: 0,
        },
        currentStep: 1,
        isSubmitting: false,
        submitError: null,
        
        // Field Updates
        updateField: (field, value) => set((state) => {
          // Update form data
          state.formData[field] = value;
          
          // Track interaction
          const now = Date.now();
          state.interactions.last_interaction = now;
          
          if (!state.interactions.field_touches[field]) {
            state.interactions.field_touches[field] = 0;
          }
          state.interactions.field_touches[field]++;
          
          // Remove from abandoned if it was there
          state.interactions.abandoned_fields = 
            state.interactions.abandoned_fields.filter(f => f !== field);
          
          // Clear validation errors for this field
          delete state.interactions.validation_errors[field];
          
          // Update completion percentage
          const requiredFields = getRequiredFields(state.formData);
          const completedFields = requiredFields.filter(f => state.formData[f]);
          state.interactions.completion_percentage = 
            (completedFields.length / requiredFields.length) * 100;
        }),
        
        updateMultipleFields: (fields) => set((state) => {
          Object.entries(fields).forEach(([key, value]) => {
            state.formData[key as keyof LeadFormData] = value;
          });
          
          state.interactions.last_interaction = Date.now();
          
          // Update completion percentage
          const requiredFields = getRequiredFields(state.formData);
          const completedFields = requiredFields.filter(f => state.formData[f]);
          state.interactions.completion_percentage = 
            (completedFields.length / requiredFields.length) * 100;
        }),
        
        // Attribution
        setAttribution: (attribution) => set((state) => {
          state.attribution = { ...state.attribution, ...attribution };
          
          // Set first visit time if not set
          if (!state.attribution.first_visit) {
            state.attribution.first_visit = new Date().toISOString();
          }
          
          // Increment page views
          state.attribution.page_views = (state.attribution.page_views || 0) + 1;
        }),
        
        // Interaction Tracking
        trackFieldInteraction: (field) => set((state) => {
          if (!state.interactions.field_times[field]) {
            state.interactions.field_times[field] = Date.now();
          }
        }),
        
        trackFieldTime: (field, time) => set((state) => {
          state.interactions.field_times[field] = time;
          state.interactions.total_time_spent += time;
        }),
        
        trackValidationError: (field, error) => set((state) => {
          if (!state.interactions.validation_errors[field]) {
            state.interactions.validation_errors[field] = [];
          }
          if (!state.interactions.validation_errors[field].includes(error)) {
            state.interactions.validation_errors[field].push(error);
          }
        }),
        
        markFieldAbandoned: (field) => set((state) => {
          if (!state.interactions.abandoned_fields.includes(field)) {
            state.interactions.abandoned_fields.push(field);
          }
        }),
        
        // Form Actions
        setCurrentStep: (step) => set({ currentStep: step }),
        
        submitForm: async () => {
          const state = get();
          set({ isSubmitting: true, submitError: null });
          
          try {
            // Prepare submission data
            const submissionData = {
              ...state.formData,
              attribution: state.attribution,
              interactions: {
                ...state.interactions,
                total_time_spent: Date.now() - state.interactions.started_at,
              },
            };
            
            // Submit to API
            const response = await fetch('/api/leads', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(submissionData),
            });
            
            if (!response.ok) {
              throw new Error('Failed to submit form');
            }
            
            const result = await response.json();
            
            set({ isSubmitting: false });
            
            // Track conversion
            if (window.analytics) {
              window.analytics.track('Lead Submitted', {
                lead_id: result.id,
                debt_amount: state.formData.debtAmount,
                completion_percentage: state.interactions.completion_percentage,
                time_spent: Date.now() - state.interactions.started_at,
              });
            }
            
            return { success: true, leadId: result.id };
          } catch (error) {
            set({ 
              isSubmitting: false, 
              submitError: error instanceof Error ? error.message : 'Unknown error' 
            });
            
            return { 
              success: false, 
              error: error instanceof Error ? error.message : 'Unknown error' 
            };
          }
        },
        
        resetForm: () => set((state) => {
          state.formData = {};
          state.interactions = {
            started_at: Date.now(),
            last_interaction: Date.now(),
            field_touches: {},
            field_times: {},
            abandoned_fields: [],
            validation_errors: {},
            total_time_spent: 0,
            completion_percentage: 0,
          };
          state.currentStep = 1;
          state.isSubmitting = false;
          state.submitError = null;
        }),
        
        // Computed Values
        getCompletionPercentage: () => {
          const state = get();
          return state.interactions.completion_percentage;
        },
        
        getRequiredFieldsStatus: () => {
          const state = get();
          const requiredFields = getRequiredFields(state.formData);
          const status: Record<string, boolean> = {};
          
          requiredFields.forEach(field => {
            status[field] = !!state.formData[field as keyof LeadFormData];
          });
          
          return status;
        },
        
        isFormValid: () => {
          const state = get();
          const requiredFields = getRequiredFields(state.formData);
          
          return requiredFields.every(field => {
            const value = state.formData[field as keyof LeadFormData];
            return value !== undefined && value !== null && value !== '';
          });
        },
        
        getTimeSpentOnField: (field) => {
          const state = get();
          return state.interactions.field_times[field] || 0;
        },
        
        getTotalTimeSpent: () => {
          const state = get();
          return Date.now() - state.interactions.started_at;
        },
      })),
      {
        name: 'lead-form-storage',
        storage: createJSONStorage(() => sessionStorage),
        partialize: (state) => ({
          formData: state.formData,
          attribution: state.attribution,
          currentStep: state.currentStep,
        }),
      }
    ),
    {
      name: 'Lead Store',
    }
  )
);

// Selector hooks for common use cases
export const useLeadFormData = () => useLeadStore((state) => state.formData);
export const useLeadAttribution = () => useLeadStore((state) => state.attribution);
export const useLeadInteractions = () => useLeadStore((state) => state.interactions);
export const useLeadFormActions = () => useLeadStore((state) => ({
  updateField: state.updateField,
  updateMultipleFields: state.updateMultipleFields,
  submitForm: state.submitForm,
  resetForm: state.resetForm,
}));

// Helper hook for form fields
export function useLeadFormField<K extends keyof LeadFormData>(
  fieldName: K
): [LeadFormData[K] | undefined, (value: LeadFormData[K]) => void] {
  const value = useLeadStore((state) => state.formData[fieldName]);
  const updateField = useLeadStore((state) => state.updateField);
  
  const setValue = (newValue: LeadFormData[K]) => {
    updateField(fieldName, newValue);
  };
  
  return [value, setValue];
}

// Analytics tracking middleware
if (typeof window !== 'undefined') {
  useLeadStore.subscribe(
    (state) => state.formData,
    (formData, previousFormData) => {
      // Track significant changes
      const significantFields: (keyof LeadFormData)[] = ['debtAmount', 'state', 'creditScore'];
      
      significantFields.forEach(field => {
        if (formData[field] !== previousFormData[field] && formData[field]) {
          if (window.analytics) {
            window.analytics.track('Form Field Completed', {
              field,
              value: field === 'debtAmount' ? 'hidden' : formData[field],
            });
          }
        }
      });
    }
  );
}