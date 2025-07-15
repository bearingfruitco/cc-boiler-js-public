// Lead store placeholder
import { create } from 'zustand';

export interface Attribution {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_term?: string;
  utm_content?: string;
  gclid?: string;
  fbclid?: string;
  [key: string]: string | undefined;
}

export interface InteractionTracking {
  firstInteraction?: Date;
  lastInteraction?: Date;
  totalInteractions: number;
  completedFields: string[];
}

export interface LeadFormData {
  name?: string;
  email?: string;
  phone?: string;
  [key: string]: any;
}

export interface LeadState {
  formData: LeadFormData;
  attribution: Attribution;
  interactions: InteractionTracking;
}

export interface LeadStore extends LeadState {
  getCompletionPercentage: () => number;
  updateFormField: (field: string, value: any) => void;
  resetForm: () => void;
}

export const useLeadStore = create<LeadStore>((set, get) => ({
  formData: {},
  attribution: {},
  interactions: {
    totalInteractions: 0,
    completedFields: []
  },
  getCompletionPercentage: () => {
    const { formData } = get();
    const fields = Object.keys(formData);
    const filledFields = fields.filter(key => formData[key]);
    return fields.length > 0 ? (filledFields.length / fields.length) * 100 : 0;
  },
  updateFormField: (field, value) => {
    set(state => ({
      formData: { ...state.formData, [field]: value },
      interactions: {
        ...state.interactions,
        totalInteractions: state.interactions.totalInteractions + 1,
        completedFields: value 
          ? [...new Set([...state.interactions.completedFields, field])]
          : state.interactions.completedFields.filter(f => f !== field)
      }
    }));
  },
  resetForm: () => {
    set({
      formData: {},
      interactions: {
        totalInteractions: 0,
        completedFields: []
      }
    });
  }
}));

export const useLeadFormActions = () => {
  const updateFormField = useLeadStore(state => state.updateFormField);
  return { updateFormField };
};

export const useLeadFormField = (field: string) => {
  const value = useLeadStore(state => state.formData[field]);
  const updateFormField = useLeadStore(state => state.updateFormField);
  return [value, (newValue: any) => updateFormField(field, newValue)] as const;
};

export const useLeadFormData = () => useLeadStore(state => state.formData);
export const useLeadAttribution = () => useLeadStore(state => state.attribution);
export const useLeadInteractions = () => useLeadStore(state => state.interactions);

// Export types are already defined above
