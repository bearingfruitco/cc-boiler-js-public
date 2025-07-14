// Lead store placeholder
import { create } from 'zustand';

interface LeadFormData {
  name?: string;
  email?: string;
  phone?: string;
  [key: string]: any;
}

interface LeadStore {
  formData: LeadFormData;
  attribution: any;
  getCompletionPercentage: () => number;
  updateFormField: (field: string, value: any) => void;
}

export const useLeadStore = create<LeadStore>((set, get) => ({
  formData: {},
  attribution: {},
  getCompletionPercentage: () => {
    const { formData } = get();
    const fields = Object.keys(formData);
    const filledFields = fields.filter(key => formData[key]);
    return fields.length > 0 ? (filledFields.length / fields.length) * 100 : 0;
  },
  updateFormField: (field, value) => {
    set(state => ({
      formData: { ...state.formData, [field]: value }
    }));
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
export const useLeadInteractions = () => ({});

export type { LeadFormData, LeadStore };
