// stores/index.ts
// Central export for all Zustand stores

// Export stores
export { useLeadStore, useLeadFormData, useLeadAttribution, useLeadInteractions, useLeadFormActions, useLeadFormField } from './lead-store';
export { useQuizStore, useQuizProgress, useQuizAnswers, useQuizAnalysis, useCurrentQuestion } from './quiz-store';
export { useAnalyticsStore, useAnalyticsSession, useAnalyticsConfig, useAnalyticsActions } from './analytics-store';

// Export types
export type { LeadFormData, Attribution, InteractionTracking, LeadState } from './lead-store';
export type { QuizAnswer, QuizStep, DebtAnalysis, QuizProgress, QuizState } from './quiz-store';
export type { AnalyticsEvent, PageView, FormInteraction, ConversionEvent, Session, AnalyticsState } from './analytics-store';

// Convenience hooks for common patterns
import { useLeadStore } from './lead-store';
import { useQuizStore } from './quiz-store';
import { useAnalyticsStore } from './analytics-store';
import { shallow } from 'zustand/shallow';

// Lead form field selector hook
export function useLeadFields<K extends keyof ReturnType<typeof useLeadStore>['formData']>(
  fields: K[]
): Pick<ReturnType<typeof useLeadStore>['formData'], K> {
  return useLeadStore(
    (state) => {
      const result = {} as Pick<ReturnType<typeof useLeadStore>['formData'], K>;
      fields.forEach(field => {
        result[field] = state.formData[field];
      });
      return result;
    },
    shallow
  );
}

// Quiz navigation hook
export function useQuizNavigation() {
  return useQuizStore(
    (state) => ({
      currentStep: state.currentStep,
      totalSteps: state.totalSteps,
      nextStep: state.nextStep,
      previousStep: state.previousStep,
      goToStep: state.goToStep,
      canProceed: state.canProceedToNext(),
    }),
    shallow
  );
}

// Combined form and quiz data hook
export function useLeadQuizData() {
  const formData = useLeadStore((state) => state.formData);
  const quizAnswers = useQuizStore((state) => state.answers);
  const attribution = useLeadStore((state) => state.attribution);
  
  return {
    formData,
    quizAnswers,
    attribution,
    getCombinedData: () => {
      // Map quiz answers to form fields
      const combinedData = { ...formData };
      
      Object.entries(quizAnswers).forEach(([stepId, answer]) => {
        const step = useQuizStore.getState().steps.find(s => s.id === parseInt(stepId));
        if (step?.field && answer.value !== undefined) {
          combinedData[step.field as keyof typeof formData] = answer.value;
        }
      });
      
      return combinedData;
    },
  };
}

// Analytics tracking hook
export function useTrackingActions() {
  const track = useAnalyticsStore((state) => state.track);
  const trackConversion = useAnalyticsStore((state) => state.trackConversion);
  const leadFormData = useLeadStore((state) => state.formData);
  const quizAnalysis = useQuizStore((state) => state.debtAnalysis);
  
  return {
    trackLeadFormStart: () => {
      track('Lead Form Started', {
        form_name: 'main_lead_form',
        entry_point: window.location.pathname,
      });
    },
    
    trackLeadFormField: (fieldName: string, value: any) => {
      track('Lead Form Field Completed', {
        field_name: fieldName,
        has_value: !!value,
        form_completion: useLeadStore.getState().getCompletionPercentage(),
      });
    },
    
    trackQuizStart: () => {
      track('Quiz Started', {
        quiz_type: 'debt_relief',
        total_steps: useQuizStore.getState().totalSteps,
      });
    },
    
    trackQuizComplete: () => {
      const analysis = useQuizStore.getState().debtAnalysis;
      track('Quiz Completed', {
        qualification_status: analysis?.qualification_status,
        financial_grade: analysis?.financial_grade,
        debt_amount: analysis?.total_debt,
        time_spent: useQuizStore.getState().getTimeSpentTotal(),
      });
    },
    
    trackLeadSubmission: (leadId: string) => {
      trackConversion('lead', leadFormData.debtAmount, {
        lead_id: leadId,
        qualification_status: quizAnalysis?.qualification_status,
        source: useLeadStore.getState().attribution.utm_source,
      });
    },
  };
}

// Reset all stores (useful for testing or logout)
export function resetAllStores() {
  useLeadStore.getState().resetForm();
  useQuizStore.getState().resetQuiz();
  useAnalyticsStore.getState().startNewSession();
}

// Debug helper
export function debugStores() {
  if (process.env.NODE_ENV === 'development') {
    console.group('🏪 Store Debug Info');
    
    console.log('Lead Store:', {
      formData: useLeadStore.getState().formData,
      attribution: useLeadStore.getState().attribution,
      completionPercentage: useLeadStore.getState().getCompletionPercentage(),
    });
    
    console.log('Quiz Store:', {
      currentStep: useQuizStore.getState().currentStep,
      answers: useQuizStore.getState().answers,
      analysis: useQuizStore.getState().debtAnalysis,
    });
    
    console.log('Analytics Store:', {
      session: useAnalyticsStore.getState().session,
      eventCount: useAnalyticsStore.getState().events.length,
      queuedEvents: useAnalyticsStore.getState().queuedEvents.length,
    });
    
    console.groupEnd();
  }
}

// Export debug function for development
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  (window as any).debugStores = debugStores;
  (window as any).resetAllStores = resetAllStores;
}