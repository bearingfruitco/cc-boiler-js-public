// Quiz store placeholder
import { create } from 'zustand';

export interface QuizAnswer {
  questionId: string;
  value: any;
  timestamp: Date;
}

export interface QuizStep {
  id: string;
  question: string;
  field?: string;
  type: 'single' | 'multiple' | 'text' | 'number';
  options?: Array<{ value: string; label: string }>;
}

export interface DebtAnalysis {
  totalDebt: number;
  monthlyPayment: number;
  qualificationStatus: 'qualified' | 'not-qualified' | 'review-needed';
  recommendations: string[];
}

export interface QuizProgress {
  currentStep: number;
  totalSteps: number;
  completedSteps: number[];
  timeSpent: number;
}

export interface QuizState {
  currentStep: number;
  totalSteps: number;
  answers: Record<string, QuizAnswer>;
  timeStarted?: Date;
  timeCompleted?: Date;
  analysis?: DebtAnalysis;
}

export interface QuizStore extends QuizState {
  nextStep: () => void;
  previousStep: () => void;
  goToStep: (step: number) => void;
  setAnswer: (questionId: string, value: any) => void;
  canProceedToNext: () => boolean;
  getTimeSpentTotal: () => number;
  resetQuiz: () => void;
}

export const useQuizStore = create<QuizStore>((set, get) => ({
  currentStep: 0,
  totalSteps: 5,
  answers: {},
  
  nextStep: () => {
    set(state => ({
      currentStep: Math.min(state.currentStep + 1, state.totalSteps - 1)
    }));
  },
  
  previousStep: () => {
    set(state => ({
      currentStep: Math.max(state.currentStep - 1, 0)
    }));
  },
  
  goToStep: (step) => {
    set({ currentStep: Math.max(0, Math.min(step, get().totalSteps - 1)) });
  },
  
  setAnswer: (questionId, value) => {
    set(state => ({
      answers: {
        ...state.answers,
        [questionId]: {
          questionId,
          value,
          timestamp: new Date()
        }
      }
    }));
  },
  
  canProceedToNext: () => {
    // Add your validation logic here
    return true;
  },
  
  getTimeSpentTotal: () => {
    const { timeStarted } = get();
    if (!timeStarted) return 0;
    return Date.now() - timeStarted.getTime();
  },
  
  resetQuiz: () => {
    set({
      currentStep: 0,
      answers: {},
      timeStarted: undefined,
      timeCompleted: undefined,
      analysis: undefined
    });
  }
}));

export const useQuizAnswers = () => useQuizStore(state => state.answers);
export const useQuizAnalysis = () => useQuizStore(state => state.analysis);
export const useQuizProgress = () => useQuizStore(state => ({
  currentStep: state.currentStep,
  totalSteps: state.totalSteps,
  completedSteps: Object.keys(state.answers).length
}));

// Export type is already defined above

// Export for compatibility
export function useCurrentQuestion() {
  const store = useQuizStore();
  return store.answers[store.currentStep];
}
