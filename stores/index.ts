// Export all store types and hooks
export * from './analytics-store';
export * from './form-store';
export * from './lead-store';
export * from './quiz-store';

// Additional stores if they exist
try {
  // @ts-ignore
  const storesIndex = await import('./stores-index');
  if (storesIndex) {
    Object.keys(storesIndex).forEach(key => {
      if (!exports[key]) {
        exports[key] = storesIndex[key];
      }
    });
  }
} catch {
  // Ignore if stores-index doesn't exist
}

// Combined hooks
import { useLeadStore } from './lead-store';
import { useQuizStore } from './quiz-store';
import { useAnalyticsStore } from './analytics-store';
import { useFormStore } from './form-store';

// Helper functions
export function useLeadFields<K extends keyof ReturnType<typeof useLeadStore>>(
  fields: K[]
): Pick<ReturnType<typeof useLeadStore>, K> {
  return useLeadStore((state) => {
    const result = {} as Pick<ReturnType<typeof useLeadStore>, K>;
    fields.forEach((field) => {
      result[field] = state[field];
    });
    return result;
  });
}

// Quiz navigation helper
export function useQuizNavigation() {
  return useQuizStore((state) => ({
    currentStep: state.currentStep,
    totalSteps: state.totalSteps,
    nextStep: state.nextStep,
    previousStep: state.previousStep,
    goToStep: state.goToStep,
    canProceed: state.canProceedToNext(),
  }));
}

// Form validation helper
export function useFormValidation() {
  const { errors, touched } = useFormStore();
  
  return {
    hasErrors: Object.keys(errors).length > 0,
    isTouched: Object.keys(touched).length > 0,
    getFieldError: (field: string) => touched[field] ? errors[field] : undefined,
  };
}

// Lead form submission helper
export function useLeadFormSubmission() {
  const leadStore = useLeadStore();
  const quizStore = useQuizStore();
  const analyticsStore = useAnalyticsStore();
  
  return async (leadId: string) => {
    // Track conversion
    analyticsStore.trackConversion('lead', leadStore.formData.debtAmount || 0);
    
    // Reset stores
    leadStore.resetForm();
    quizStore.resetQuiz();
    
    return leadId;
  };
}

// Debug helper
export function useStoreDebug() {
  const lead = useLeadStore();
  const quiz = useQuizStore();
  const analytics = useAnalyticsStore();
  const form = useFormStore();
  
  return {
    stores: {
      lead: {
        formData: lead.formData,
        attribution: lead.attribution,
        completion: lead.getCompletionPercentage(),
      },
      quiz: {
        currentStep: quiz.currentStep,
        totalSteps: quiz.totalSteps,
        answers: quiz.answers,
      },
      analytics: {
        isInitialized: analytics.isInitialized,
      },
      form: {
        data: form.formData,
        errors: form.errors,
        isSubmitting: form.isSubmitting,
      },
    },
  };
}
