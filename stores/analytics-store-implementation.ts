// stores/analytics-store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { subscribeWithSelector } from 'zustand/middleware';

interface AnalyticsEvent {
  event_id: string;
  event_name: string;
  event_category: 'page' | 'form' | 'quiz' | 'conversion' | 'error' | 'custom';
  properties: Record<string, any>;
  timestamp: string;
  session_id: string;
  user_id?: string;
}

interface PageView {
  page_id: string;
  path: string;
  title: string;
  referrer: string;
  timestamp: string;
  time_on_page?: number;
  exit_rate?: number;
  bounce?: boolean;
}

interface FormInteraction {
  form_name: string;
  field_name: string;
  interaction_type: 'focus' | 'blur' | 'change' | 'error' | 'submit';
  value_length?: number;
  time_spent?: number;
  error_message?: string;
  timestamp: string;
}

interface ConversionEvent {
  conversion_id: string;
  conversion_type: 'lead' | 'signup' | 'purchase' | 'custom';
  conversion_value?: number;
  attribution: {
    source?: string;
    medium?: string;
    campaign?: string;
    content?: string;
    term?: string;
  };
  metadata: Record<string, any>;
  timestamp: string;
}

interface Session {
  session_id: string;
  started_at: string;
  last_activity: string;
  page_views: number;
  events_count: number;
  duration: number;
  is_bounce: boolean;
  device_info: {
    browser: string;
    os: string;
    device_type: 'mobile' | 'tablet' | 'desktop';
    screen_resolution: string;
  };
}

interface AnalyticsState {
  // Session Management
  session: Session;
  userId?: string;
  anonymousId: string;
  
  // Event Tracking
  events: AnalyticsEvent[];
  queuedEvents: AnalyticsEvent[];
  failedEvents: AnalyticsEvent[];
  
  // Page Tracking
  pageViews: PageView[];
  currentPage?: PageView;
  
  // Form Tracking
  formInteractions: FormInteraction[];
  formCompletions: Record<string, number>;
  
  // Conversion Tracking
  conversions: ConversionEvent[];
  goals: Record<string, boolean>;
  
  // Configuration
  config: {
    endpoint: string;
    flushInterval: number;
    batchSize: number;
    debug: boolean;
    enabledProviders: string[];
  };
  
  // Actions - Core
  identify: (userId: string, traits?: Record<string, any>) => void;
  track: (eventName: string, properties?: Record<string, any>, category?: AnalyticsEvent['event_category']) => void;
  page: (pageName?: string, properties?: Record<string, any>) => void;
  
  // Actions - Form Tracking
  trackFormInteraction: (formName: string, fieldName: string, interactionType: FormInteraction['interaction_type'], data?: any) => void;
  trackFormCompletion: (formName: string, data?: Record<string, any>) => void;
  
  // Actions - Conversion Tracking
  trackConversion: (type: ConversionEvent['conversion_type'], value?: number, metadata?: Record<string, any>) => void;
  setGoal: (goalName: string, achieved: boolean) => void;
  
  // Actions - Session Management
  startNewSession: () => void;
  endSession: () => void;
  updateSessionActivity: () => void;
  
  // Actions - Queue Management
  flush: () => Promise<void>;
  retry: () => Promise<void>;
  clear: () => void;
  
  // Computed Values
  getSessionDuration: () => number;
  getEventCount: () => number;
  getConversionRate: (conversionType?: string) => number;
  getFormCompletionRate: (formName: string) => number;
}

// Helper functions
function generateId(): string {
  return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

function generateSessionId(): string {
  return `session_${generateId()}`;
}

function getDeviceInfo() {
  const ua = navigator.userAgent;
  const mobile = /Mobile|Android|iPhone/i.test(ua);
  const tablet = /iPad|Tablet/i.test(ua);
  
  return {
    browser: getBrowser(ua),
    os: getOS(ua),
    device_type: mobile ? 'mobile' : tablet ? 'tablet' : 'desktop' as const,
    screen_resolution: `${window.screen.width}x${window.screen.height}`,
  };
}

function getBrowser(ua: string): string {
  if (ua.includes('Chrome')) return 'Chrome';
  if (ua.includes('Firefox')) return 'Firefox';
  if (ua.includes('Safari')) return 'Safari';
  if (ua.includes('Edge')) return 'Edge';
  return 'Other';
}

function getOS(ua: string): string {
  if (ua.includes('Windows')) return 'Windows';
  if (ua.includes('Mac')) return 'macOS';
  if (ua.includes('Linux')) return 'Linux';
  if (ua.includes('Android')) return 'Android';
  if (ua.includes('iOS')) return 'iOS';
  return 'Other';
}

// Create the store
export const useAnalyticsStore = create<AnalyticsState>()(
  devtools(
    subscribeWithSelector(
      (set, get) => ({
        // Initial State
        session: {
          session_id: generateSessionId(),
          started_at: new Date().toISOString(),
          last_activity: new Date().toISOString(),
          page_views: 0,
          events_count: 0,
          duration: 0,
          is_bounce: true,
          device_info: getDeviceInfo(),
        },
        anonymousId: generateId(),
        events: [],
        queuedEvents: [],
        failedEvents: [],
        pageViews: [],
        formInteractions: [],
        formCompletions: {},
        conversions: [],
        goals: {},
        config: {
          endpoint: '/api/analytics',
          flushInterval: 30000, // 30 seconds
          batchSize: 50,
          debug: process.env.NODE_ENV === 'development',
          enabledProviders: ['rudderstack', 'google', 'facebook'],
        },
        
        // Core Actions
        identify: (userId, traits = {}) => {
          set({ userId });
          
          const event: AnalyticsEvent = {
            event_id: generateId(),
            event_name: 'User Identified',
            event_category: 'custom',
            properties: {
              user_id: userId,
              traits,
              anonymous_id: get().anonymousId,
            },
            timestamp: new Date().toISOString(),
            session_id: get().session.session_id,
            user_id: userId,
          };
          
          set((state) => ({
            events: [...state.events, event],
            queuedEvents: [...state.queuedEvents, event],
          }));
          
          // Send to providers
          if (window.analytics) {
            window.analytics.identify(userId, traits);
          }
        },
        
        track: (eventName, properties = {}, category = 'custom') => {
          const state = get();
          const event: AnalyticsEvent = {
            event_id: generateId(),
            event_name: eventName,
            event_category: category,
            properties: {
              ...properties,
              session_id: state.session.session_id,
              page_path: window.location.pathname,
              page_title: document.title,
            },
            timestamp: new Date().toISOString(),
            session_id: state.session.session_id,
            user_id: state.userId,
          };
          
          set((state) => ({
            events: [...state.events, event],
            queuedEvents: [...state.queuedEvents, event],
            session: {
              ...state.session,
              events_count: state.session.events_count + 1,
              last_activity: new Date().toISOString(),
              is_bounce: false,
            },
          }));
          
          // Send to providers
          if (window.analytics) {
            window.analytics.track(eventName, event.properties);
          }
          
          // Log in debug mode
          if (state.config.debug) {
            console.log('[Analytics] Track:', eventName, properties);
          }
        },
        
        page: (pageName, properties = {}) => {
          const pageView: PageView = {
            page_id: generateId(),
            path: window.location.pathname,
            title: pageName || document.title,
            referrer: document.referrer,
            timestamp: new Date().toISOString(),
          };
          
          set((state) => {
            // Calculate time on previous page
            if (state.currentPage) {
              const timeOnPage = Date.now() - new Date(state.currentPage.timestamp).getTime();
              state.currentPage.time_on_page = timeOnPage;
            }
            
            return {
              pageViews: [...state.pageViews, pageView],
              currentPage: pageView,
              session: {
                ...state.session,
                page_views: state.session.page_views + 1,
                last_activity: new Date().toISOString(),
              },
            };
          });
          
          // Track as event
          get().track('Page Viewed', {
            ...properties,
            page_path: pageView.path,
            page_title: pageView.title,
            referrer: pageView.referrer,
          }, 'page');
          
          // Send to providers
          if (window.analytics) {
            window.analytics.page(pageName, properties);
          }
        },
        
        // Form Tracking
        trackFormInteraction: (formName, fieldName, interactionType, data = {}) => {
          const interaction: FormInteraction = {
            form_name: formName,
            field_name: fieldName,
            interaction_type: interactionType,
            timestamp: new Date().toISOString(),
            ...data,
          };
          
          set((state) => ({
            formInteractions: [...state.formInteractions, interaction],
          }));
          
          // Track as event
          get().track('Form Field Interacted', {
            form_name: formName,
            field_name: fieldName,
            interaction_type: interactionType,
            ...data,
          }, 'form');
        },
        
        trackFormCompletion: (formName, data = {}) => {
          set((state) => ({
            formCompletions: {
              ...state.formCompletions,
              [formName]: (state.formCompletions[formName] || 0) + 1,
            },
          }));
          
          // Track as event
          get().track('Form Completed', {
            form_name: formName,
            ...data,
          }, 'form');
        },
        
        // Conversion Tracking
        trackConversion: (type, value, metadata = {}) => {
          const conversion: ConversionEvent = {
            conversion_id: generateId(),
            conversion_type: type,
            conversion_value: value,
            attribution: {
              source: new URLSearchParams(window.location.search).get('utm_source') || undefined,
              medium: new URLSearchParams(window.location.search).get('utm_medium') || undefined,
              campaign: new URLSearchParams(window.location.search).get('utm_campaign') || undefined,
            },
            metadata,
            timestamp: new Date().toISOString(),
          };
          
          set((state) => ({
            conversions: [...state.conversions, conversion],
          }));
          
          // Track as event
          get().track('Conversion', {
            conversion_type: type,
            conversion_value: value,
            ...metadata,
          }, 'conversion');
          
          // Send to conversion APIs
          if (window.fbq && type === 'lead') {
            window.fbq('track', 'Lead', { value });
          }
          
          if (window.gtag) {
            window.gtag('event', 'conversion', {
              send_to: 'YOUR_CONVERSION_ID',
              value,
              currency: 'USD',
            });
          }
        },
        
        setGoal: (goalName, achieved) => {
          set((state) => ({
            goals: {
              ...state.goals,
              [goalName]: achieved,
            },
          }));
          
          if (achieved) {
            get().track('Goal Achieved', { goal_name: goalName });
          }
        },
        
        // Session Management
        startNewSession: () => {
          const newSession: Session = {
            session_id: generateSessionId(),
            started_at: new Date().toISOString(),
            last_activity: new Date().toISOString(),
            page_views: 0,
            events_count: 0,
            duration: 0,
            is_bounce: true,
            device_info: getDeviceInfo(),
          };
          
          set({
            session: newSession,
            events: [],
            pageViews: [],
            formInteractions: [],
          });
        },
        
        endSession: () => {
          const state = get();
          const duration = Date.now() - new Date(state.session.started_at).getTime();
          
          // Track session end
          get().track('Session Ended', {
            duration,
            page_views: state.session.page_views,
            events_count: state.session.events_count,
            is_bounce: state.session.is_bounce,
          });
          
          // Flush remaining events
          get().flush();
        },
        
        updateSessionActivity: () => {
          set((state) => ({
            session: {
              ...state.session,
              last_activity: new Date().toISOString(),
              duration: Date.now() - new Date(state.session.started_at).getTime(),
            },
          }));
        },
        
        // Queue Management
        flush: async () => {
          const state = get();
          if (state.queuedEvents.length === 0) return;
          
          const eventsToSend = [...state.queuedEvents];
          set({ queuedEvents: [] });
          
          try {
            const response = await fetch(state.config.endpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                events: eventsToSend,
                session: state.session,
                user_id: state.userId,
                anonymous_id: state.anonymousId,
              }),
            });
            
            if (!response.ok) {
              throw new Error('Failed to send analytics');
            }
            
            if (state.config.debug) {
              console.log('[Analytics] Flushed', eventsToSend.length, 'events');
            }
          } catch (error) {
            // Add to failed events for retry
            set((state) => ({
              failedEvents: [...state.failedEvents, ...eventsToSend],
            }));
            
            console.error('[Analytics] Flush failed:', error);
          }
        },
        
        retry: async () => {
          const state = get();
          if (state.failedEvents.length === 0) return;
          
          const eventsToRetry = [...state.failedEvents];
          set({ failedEvents: [] });
          
          // Add back to queue
          set((state) => ({
            queuedEvents: [...state.queuedEvents, ...eventsToRetry],
          }));
          
          // Try to flush
          await get().flush();
        },
        
        clear: () => {
          set({
            events: [],
            queuedEvents: [],
            failedEvents: [],
            pageViews: [],
            formInteractions: [],
            conversions: [],
          });
        },
        
        // Computed Values
        getSessionDuration: () => {
          const state = get();
          return Date.now() - new Date(state.session.started_at).getTime();
        },
        
        getEventCount: () => {
          const state = get();
          return state.events.length;
        },
        
        getConversionRate: (conversionType) => {
          const state = get();
          const relevantConversions = conversionType
            ? state.conversions.filter(c => c.conversion_type === conversionType)
            : state.conversions;
          
          if (state.session.page_views === 0) return 0;
          
          return (relevantConversions.length / state.session.page_views) * 100;
        },
        
        getFormCompletionRate: (formName) => {
          const state = get();
          const interactions = state.formInteractions.filter(i => i.form_name === formName && i.interaction_type === 'focus');
          const completions = state.formCompletions[formName] || 0;
          
          if (interactions.length === 0) return 0;
          
          return (completions / interactions.length) * 100;
        },
      })
    ),
    {
      name: 'Analytics Store',
    }
  )
);

// Auto-flush interval
if (typeof window !== 'undefined') {
  setInterval(() => {
    const store = useAnalyticsStore.getState();
    if (store.queuedEvents.length > 0) {
      store.flush();
    }
  }, 30000); // Every 30 seconds
  
  // Flush on page unload
  window.addEventListener('beforeunload', () => {
    useAnalyticsStore.getState().flush();
  });
  
  // Track page visibility changes
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      useAnalyticsStore.getState().flush();
    } else {
      useAnalyticsStore.getState().updateSessionActivity();
    }
  });
  
  // Session timeout (30 minutes of inactivity)
  let sessionTimeout: NodeJS.Timeout;
  
  const resetSessionTimeout = () => {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(() => {
      useAnalyticsStore.getState().startNewSession();
    }, 30 * 60 * 1000); // 30 minutes
  };
  
  // Reset timeout on any activity
  ['click', 'scroll', 'keypress'].forEach(event => {
    document.addEventListener(event, () => {
      useAnalyticsStore.getState().updateSessionActivity();
      resetSessionTimeout();
    });
  });
  
  resetSessionTimeout();
}

// Export convenience hooks
export const useAnalyticsSession = () => useAnalyticsStore((state) => state.session);
export const useAnalyticsConfig = () => useAnalyticsStore((state) => state.config);
export const useAnalyticsActions = () => useAnalyticsStore((state) => ({
  track: state.track,
  page: state.page,
  identify: state.identify,
  trackConversion: state.trackConversion,
}));