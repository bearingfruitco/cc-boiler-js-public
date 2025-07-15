import { create } from 'zustand';
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

interface FormData {
  [key: string]: any;
}

interface FormStore {
  formData: FormData;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
  isSubmitting: boolean;
  
  // Core methods
  updateFormField: (field: string, value: any) => void;
  updateMultipleFields: (fields: Record<string, any>) => void;
  setFieldError: (field: string, error: string) => void;
  clearFieldError: (field: string) => void;
  setFieldTouched: (field: string) => void;
  resetForm: () => void;
  setSubmitting: (isSubmitting: boolean) => void;
  
  // Event tracking methods
  trackFieldInteraction: (field: string, eventType: 'focus' | 'blur' | 'change') => void;
}

export const useFormStore = create<FormStore>((set, get) => ({
  formData: {},
  errors: {},
  touched: {},
  isSubmitting: false,
  
  updateFormField: (field, value) => {
    const oldValue = get().formData[field];
    
    set((state) => ({
      formData: { ...state.formData, [field]: value }
    }));
    
    // Emit field change event
    eventQueue.emit(LEAD_EVENTS.FIELD_CHANGE, {
      fieldName: field,
      oldValue,
      newValue: value,
      timestamp: new Date().toISOString(),
    });
  },
  
  updateMultipleFields: (fields) => {
    set((state) => ({
      formData: { ...state.formData, ...fields }
    }));
    
    // Track each field change
    Object.entries(fields).forEach(([field, value]) => {
      const oldValue = get().formData[field];
      eventQueue.emit(LEAD_EVENTS.FIELD_CHANGE, {
        fieldName: field,
        oldValue,
        newValue: value,
        timestamp: new Date().toISOString(),
      });
    });
  },
  
  setFieldError: (field, error) => {
    set((state) => ({
      errors: { ...state.errors, [field]: error }
    }));
  },
  
  clearFieldError: (field) => {
    set((state) => {
      const errors = { ...state.errors };
      delete errors[field];
      return { errors };
    });
  },
  
  setFieldTouched: (field) => {
    set((state) => ({
      touched: { ...state.touched, [field]: true }
    }));
  },
  
  resetForm: () => {
    set({
      formData: {},
      errors: {},
      touched: {},
      isSubmitting: false
    });
  },
  
  setSubmitting: (isSubmitting) => {
    set({ isSubmitting });
  },
  
  trackFieldInteraction: (field, eventType) => {
    const eventMap = {
      focus: LEAD_EVENTS.FIELD_FOCUS,
      blur: LEAD_EVENTS.FIELD_BLUR,
      change: LEAD_EVENTS.FIELD_CHANGE,
    };
    
    eventQueue.emit(eventMap[eventType], {
      fieldName: field,
      timestamp: new Date().toISOString(),
    });
  }
}));

// Alias for backward compatibility
export const useFormState = useFormStore;
