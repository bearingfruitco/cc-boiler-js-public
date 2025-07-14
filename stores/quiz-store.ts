// Quiz store placeholder
import { create } from 'zustand';

interface QuizStore {
  steps: any[];
  answers: any;
  debtAnalysis: any;
}

export const useQuizStore = create<QuizStore>(() => ({
  steps: [],
  answers: {},
  debtAnalysis: null
}));

export const useQuizProgress = () => ({});
export const useQuizAnswers = () => useQuizStore(state => state.answers);
export const useQuizAnalysis = () => useQuizStore(state => state.debtAnalysis);
export const useCurrentQuestion = () => null;

export type { QuizStore };
