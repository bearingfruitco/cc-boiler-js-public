// stores/quiz-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { subscribeWithSelector } from 'zustand/middleware';
import { devtools } from 'zustand/middleware';

interface QuizAnswer {
  value: any;
  answeredAt: number;
  timeSpent: number;
}

interface QuizStep {
  id: number;
  question: string;
  type: 'single-choice' | 'multiple-choice' | 'range' | 'input' | 'yes-no';
  field: string;
  options?: Array<{ value: any; label: string; description?: string }>;
  validation?: {
    required?: boolean;
    min?: number;
    max?: number;
    pattern?: RegExp;
  };
}

interface DebtAnalysis {
  total_debt: number;
  monthly_payment: number;
  monthly_income: number;
  debt_to_income: number;
  credit_utilization: number;
  qualification_status: 'qualified' | 'not_qualified' | 'needs_review';
  qualification_reasons: string[];
  recommended_solutions: Array<{
    type: 'settlement' | 'consolidation' | 'counseling' | 'diy';
    name: string;
    description: string;
    pros: string[];
    cons: string[];
    estimated_savings?: number;
    estimated_timeline?: string;
  }>;
  financial_grade: 'A' | 'B' | 'C' | 'D' | 'F';
  risk_score: number; // 0-100
}

interface QuizProgress {
  started_at: number;
  completed_at?: number;
  last_activity: number;
  time_per_step: Record<number, number>;
  step_attempts: Record<number, number>;
  abandoned_step?: number;
  total_time: number;
  backtrack_count: number;
}

interface QuizState {
  // Quiz Configuration
  steps: QuizStep[];
  currentStep: number;
  totalSteps: number;
  
  // Answers & Progress
  answers: Record<number, QuizAnswer>;
  progress: QuizProgress;
  
  // Analysis Results
  debtAnalysis?: DebtAnalysis;
  qualificationResult?: {
    qualified: boolean;
    reasons: string[];
    next_steps: string[];
  };
  
  // UI State
  isCalculating: boolean;
  showResults: boolean;
  error: string | null;
  
  // Actions - Navigation
  nextStep: () => void;
  previousStep: () => void;
  goToStep: (step: number) => void;
  
  // Actions - Answers
  setAnswer: (step: number, value: any) => void;
  updateAnswer: (step: number, value: any) => void;
  
  // Actions - Analysis
  calculateDebtAnalysis: () => Promise<void>;
  getRecommendations: () => void;
  
  // Actions - State Management
  completeQuiz: () => void;
  resetQuiz: () => void;
  saveProgress: () => void;
  
  // Computed Values
  getCurrentQuestion: () => QuizStep | undefined;
  getProgressPercentage: () => number;
  isStepCompleted: (step: number) => boolean;
  canProceedToNext: () => boolean;
  getAnswerForStep: (step: number) => any;
  getTimeSpentTotal: () => number;
}

// Default quiz steps for debt relief
const DEFAULT_QUIZ_STEPS: QuizStep[] = [
  {
    id: 1,
    question: "How much total debt do you have?",
    type: 'range',
    field: 'debtAmount',
    validation: { required: true, min: 0, max: 1000000 },
  },
  {
    id: 2,
    question: "What types of debt do you have?",
    type: 'multiple-choice',
    field: 'debtTypes',
    options: [
      { value: 'credit_card', label: 'Credit Cards' },
      { value: 'medical', label: 'Medical Bills' },
      { value: 'personal_loan', label: 'Personal Loans' },
      { value: 'student_loan', label: 'Student Loans' },
      { value: 'auto_loan', label: 'Auto Loans' },
      { value: 'other', label: 'Other' },
    ],
    validation: { required: true },
  },
  {
    id: 3,
    question: "What's your credit score range?",
    type: 'single-choice',
    field: 'creditScore',
    options: [
      { value: 'excellent', label: '740+', description: 'Excellent' },
      { value: 'good', label: '670-739', description: 'Good' },
      { value: 'fair', label: '580-669', description: 'Fair' },
      { value: 'poor', label: 'Below 580', description: 'Poor' },
      { value: 'unknown', label: "I don't know" },
    ],
    validation: { required: true },
  },
  {
    id: 4,
    question: "What's your monthly income?",
    type: 'input',
    field: 'monthlyIncome',
    validation: { required: true, min: 0, max: 100000 },
  },
  {
    id: 5,
    question: "Are you behind on any payments?",
    type: 'yes-no',
    field: 'behindOnPayments',
    validation: { required: true },
  },
  {
    id: 6,
    question: "What state do you live in?",
    type: 'single-choice',
    field: 'state',
    options: [
      { value: 'CA', label: 'California' },
      { value: 'TX', label: 'Texas' },
      { value: 'FL', label: 'Florida' },
      { value: 'NY', label: 'New York' },
      // ... add all states
    ],
    validation: { required: true },
  },
  {
    id: 7,
    question: "Have you filed for bankruptcy in the last 7 years?",
    type: 'yes-no',
    field: 'filedBankruptcy',
    validation: { required: true },
  },
];

// Helper functions
function calculateFinancialGrade(dti: number): 'A' | 'B' | 'C' | 'D' | 'F' {
  if (dti < 20) return 'A';
  if (dti < 36) return 'B';
  if (dti < 43) return 'C';
  if (dti < 50) return 'D';
  return 'F';
}

function calculateRiskScore(analysis: Partial<DebtAnalysis>): number {
  let score = 100;
  
  // Debt to income ratio impact
  if (analysis.debt_to_income) {
    score -= Math.min(analysis.debt_to_income * 0.5, 40);
  }
  
  // Credit utilization impact
  if (analysis.credit_utilization) {
    score -= Math.min(analysis.credit_utilization * 0.3, 30);
  }
  
  return Math.max(0, Math.round(score));
}

// Create the store
export const useQuizStore = create<QuizState>()(
  devtools(
    subscribeWithSelector(
      persist(
        (set, get) => ({
          // Initial State
          steps: DEFAULT_QUIZ_STEPS,
          currentStep: 1,
          totalSteps: DEFAULT_QUIZ_STEPS.length,
          answers: {},
          progress: {
            started_at: Date.now(),
            last_activity: Date.now(),
            time_per_step: {},
            step_attempts: {},
            total_time: 0,
            backtrack_count: 0,
          },
          isCalculating: false,
          showResults: false,
          error: null,
          
          // Navigation Actions
          nextStep: () => set((state) => {
            const newStep = Math.min(state.currentStep + 1, state.totalSteps);
            
            // Track time spent on current step
            const timeSpent = Date.now() - (state.progress.time_per_step[state.currentStep] || state.progress.started_at);
            
            return {
              currentStep: newStep,
              progress: {
                ...state.progress,
                last_activity: Date.now(),
                time_per_step: {
                  ...state.progress.time_per_step,
                  [state.currentStep]: timeSpent,
                },
              },
            };
          }),
          
          previousStep: () => set((state) => ({
            currentStep: Math.max(state.currentStep - 1, 1),
            progress: {
              ...state.progress,
              last_activity: Date.now(),
              backtrack_count: state.progress.backtrack_count + 1,
            },
          })),
          
          goToStep: (step) => set((state) => ({
            currentStep: Math.min(Math.max(step, 1), state.totalSteps),
            progress: {
              ...state.progress,
              last_activity: Date.now(),
            },
          })),
          
          // Answer Actions
          setAnswer: (step, value) => set((state) => {
            const answeredAt = Date.now();
            const timeSpent = answeredAt - (state.answers[step]?.answeredAt || state.progress.started_at);
            
            // Track attempts
            const attempts = state.progress.step_attempts[step] || 0;
            
            return {
              answers: {
                ...state.answers,
                [step]: {
                  value,
                  answeredAt,
                  timeSpent,
                },
              },
              progress: {
                ...state.progress,
                last_activity: answeredAt,
                step_attempts: {
                  ...state.progress.step_attempts,
                  [step]: attempts + 1,
                },
              },
            };
          }),
          
          updateAnswer: (step, value) => set((state) => ({
            answers: {
              ...state.answers,
              [step]: {
                ...state.answers[step],
                value,
              },
            },
          })),
          
          // Analysis Actions
          calculateDebtAnalysis: async () => {
            set({ isCalculating: true, error: null });
            
            try {
              const state = get();
              const answers = state.answers;
              
              // Extract answer values
              const debtAmount = answers[1]?.value || 0;
              const monthlyIncome = answers[4]?.value || 0;
              const creditScore = answers[3]?.value;
              const debtTypes = answers[2]?.value || [];
              const behindOnPayments = answers[5]?.value;
              
              // Calculate key metrics
              const monthlyPayment = debtAmount * 0.025; // 2.5% minimum payment estimate
              const debtToIncome = monthlyIncome > 0 ? (monthlyPayment / monthlyIncome) * 100 : 0;
              const creditUtilization = debtAmount > 30000 ? 90 : (debtAmount / 30000) * 100;
              
              // Determine qualification status
              let qualificationStatus: DebtAnalysis['qualification_status'] = 'needs_review';
              const qualificationReasons: string[] = [];
              
              if (debtAmount >= 10000 && debtToIncome > 15) {
                qualificationStatus = 'qualified';
                qualificationReasons.push('Debt amount meets minimum requirements');
                qualificationReasons.push('Debt-to-income ratio indicates financial hardship');
              } else if (debtAmount < 5000) {
                qualificationStatus = 'not_qualified';
                qualificationReasons.push('Debt amount below minimum threshold');
              }
              
              // Generate recommendations
              const recommendations: DebtAnalysis['recommended_solutions'] = [];
              
              if (qualificationStatus === 'qualified') {
                recommendations.push({
                  type: 'settlement',
                  name: 'Debt Settlement Program',
                  description: 'Negotiate to pay less than you owe',
                  pros: [
                    'Reduce total debt by 40-60%',
                    'Become debt-free in 24-48 months',
                    'One affordable monthly payment',
                  ],
                  cons: [
                    'May impact credit score temporarily',
                    'Requires stopping payments to creditors',
                  ],
                  estimated_savings: debtAmount * 0.5,
                  estimated_timeline: '24-48 months',
                });
              }
              
              if (creditScore === 'good' || creditScore === 'excellent') {
                recommendations.push({
                  type: 'consolidation',
                  name: 'Debt Consolidation Loan',
                  description: 'Combine debts into one lower payment',
                  pros: [
                    'Lower interest rate',
                    'Single monthly payment',
                    'No credit impact',
                  ],
                  cons: [
                    'Requires good credit',
                    'May extend repayment period',
                  ],
                  estimated_savings: debtAmount * 0.2,
                  estimated_timeline: '36-60 months',
                });
              }
              
              recommendations.push({
                type: 'counseling',
                name: 'Credit Counseling',
                description: 'Work with counselors to manage debt',
                pros: [
                  'Professional guidance',
                  'Budgeting assistance',
                  'Creditor negotiations',
                ],
                cons: [
                  'Monthly fees',
                  'Longer repayment timeline',
                ],
                estimated_timeline: '48-60 months',
              });
              
              const analysis: DebtAnalysis = {
                total_debt: debtAmount,
                monthly_payment: monthlyPayment,
                monthly_income: monthlyIncome,
                debt_to_income: debtToIncome,
                credit_utilization: creditUtilization,
                qualification_status: qualificationStatus,
                qualification_reasons: qualificationReasons,
                recommended_solutions: recommendations,
                financial_grade: calculateFinancialGrade(debtToIncome),
                risk_score: calculateRiskScore({ debt_to_income: debtToIncome, credit_utilization: creditUtilization }),
              };
              
              set({
                debtAnalysis: analysis,
                isCalculating: false,
                showResults: true,
              });
              
              // Track completion
              if (window.analytics) {
                window.analytics.track('Quiz Completed', {
                  debt_amount: debtAmount,
                  qualification_status: qualificationStatus,
                  financial_grade: analysis.financial_grade,
                  time_spent: Date.now() - state.progress.started_at,
                });
              }
              
            } catch (error) {
              set({
                error: error instanceof Error ? error.message : 'Failed to calculate analysis',
                isCalculating: false,
              });
            }
          },
          
          getRecommendations: () => {
            const state = get();
            return state.debtAnalysis?.recommended_solutions || [];
          },
          
          // State Management
          completeQuiz: () => set((state) => ({
            progress: {
              ...state.progress,
              completed_at: Date.now(),
              total_time: Date.now() - state.progress.started_at,
            },
          })),
          
          resetQuiz: () => set({
            currentStep: 1,
            answers: {},
            progress: {
              started_at: Date.now(),
              last_activity: Date.now(),
              time_per_step: {},
              step_attempts: {},
              total_time: 0,
              backtrack_count: 0,
            },
            debtAnalysis: undefined,
            qualificationResult: undefined,
            isCalculating: false,
            showResults: false,
            error: null,
          }),
          
          saveProgress: () => {
            const state = get();
            // Progress is automatically saved by persist middleware
            // This method can be used for explicit saves or API sync
            console.log('Quiz progress saved', {
              step: state.currentStep,
              answers: Object.keys(state.answers).length,
            });
          },
          
          // Computed Values
          getCurrentQuestion: () => {
            const state = get();
            return state.steps.find(step => step.id === state.currentStep);
          },
          
          getProgressPercentage: () => {
            const state = get();
            return (state.currentStep / state.totalSteps) * 100;
          },
          
          isStepCompleted: (step) => {
            const state = get();
            return !!state.answers[step]?.value;
          },
          
          canProceedToNext: () => {
            const state = get();
            const currentQuestion = state.steps.find(s => s.id === state.currentStep);
            
            if (!currentQuestion?.validation?.required) {
              return true;
            }
            
            const answer = state.answers[state.currentStep];
            return !!answer?.value;
          },
          
          getAnswerForStep: (step) => {
            const state = get();
            return state.answers[step]?.value;
          },
          
          getTimeSpentTotal: () => {
            const state = get();
            return Date.now() - state.progress.started_at;
          },
        }),
        {
          name: 'quiz-progress',
          partialize: (state) => ({
            currentStep: state.currentStep,
            answers: state.answers,
            progress: state.progress,
          }),
        }
      )
    ),
    {
      name: 'Quiz Store',
    }
  )
);

// Selector hooks
export const useQuizProgress = () => useQuizStore((state) => ({
  currentStep: state.currentStep,
  totalSteps: state.totalSteps,
  percentage: state.getProgressPercentage(),
  canProceed: state.canProceedToNext(),
}));

export const useQuizAnswers = () => useQuizStore((state) => state.answers);
export const useQuizAnalysis = () => useQuizStore((state) => state.debtAnalysis);
export const useCurrentQuestion = () => useQuizStore((state) => state.getCurrentQuestion());

// Analytics middleware
useQuizStore.subscribe(
  (state) => state.currentStep,
  (currentStep) => {
    if (window.analytics) {
      window.analytics.track('Quiz Step Viewed', {
        step: currentStep,
        timestamp: new Date().toISOString(),
      });
    }
  }
);