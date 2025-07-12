import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// User store with persistence
interface User {
  id: string;
  email: string;
  name?: string;
}

interface UserState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  devtools(
    persist(
      immer((set) => ({
        user: null,
        isLoading: false,
        error: null,
        setUser: (user) =>
          set((state) => {
            state.user = user;
            state.error = null;
          }),
        setLoading: (loading) =>
          set((state) => {
            state.isLoading = loading;
          }),
        setError: (error) =>
          set((state) => {
            state.error = error;
            state.isLoading = false;
          }),
        logout: () =>
          set((state) => {
            state.user = null;
            state.error = null;
            state.isLoading = false;
          }),
      })),
      {
        name: 'user-store',
        partialize: (state) => ({ user: state.user }), // Only persist user
      }
    ),
    {
      name: 'UserStore',
    }
  )
);

// UI Store (no persistence)
interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark' | 'system';
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}

export const useUIStore = create<UIState>()(
  devtools(
    immer((set) => ({
      sidebarOpen: false,
      theme: 'system',
      toggleSidebar: () =>
        set((state) => {
          state.sidebarOpen = !state.sidebarOpen;
        }),
      setSidebarOpen: (open) =>
        set((state) => {
          state.sidebarOpen = open;
        }),
      setTheme: (theme) =>
        set((state) => {
          state.theme = theme;
        }),
    })),
    {
      name: 'UIStore',
    }
  )
);

// Form store with field tracking
interface FormField {
  value: string | number | boolean;
  error?: string;
  touched: boolean;
  pii?: boolean;
}

interface FormState {
  fields: Record<string, FormField>;
  isSubmitting: boolean;
  submitError: string | null;
  setField: (name: string, value: any) => void;
  setFieldError: (name: string, error: string | undefined) => void;
  touchField: (name: string) => void;
  setSubmitting: (submitting: boolean) => void;
  setSubmitError: (error: string | null) => void;
  reset: () => void;
}

export const useFormStore = create<FormState>()(
  devtools(
    immer((set) => ({
      fields: {},
      isSubmitting: false,
      submitError: null,
      setField: (name, value) =>
        set((state) => {
          if (!state.fields[name]) {
            state.fields[name] = { value, touched: false };
          } else {
            state.fields[name].value = value;
            state.fields[name].touched = true;
          }
        }),
      setFieldError: (name, error) =>
        set((state) => {
          if (state.fields[name]) {
            state.fields[name].error = error;
          }
        }),
      touchField: (name) =>
        set((state) => {
          if (state.fields[name]) {
            state.fields[name].touched = true;
          }
        }),
      setSubmitting: (submitting) =>
        set((state) => {
          state.isSubmitting = submitting;
        }),
      setSubmitError: (error) =>
        set((state) => {
          state.submitError = error;
          state.isSubmitting = false;
        }),
      reset: () =>
        set((state) => {
          state.fields = {};
          state.isSubmitting = false;
          state.submitError = null;
        }),
    })),
    {
      name: 'FormStore',
    }
  )
);
