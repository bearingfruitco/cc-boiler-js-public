/**
 * CAPTCHA Component for form protection
 * Uses Google reCAPTCHA v3 for invisible verification
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import Script from 'next/script';

interface ReCAPTCHAProps {
  siteKey: string;
  onChange: (token: string) => void;
  onError?: (error: Error) => void;
  action?: string;
}

declare global {
  interface Window {
    grecaptcha: any;
    onRecaptchaLoad?: () => void;
  }
}

export function ReCAPTCHA({ 
  siteKey, 
  onChange, 
  onError,
  action = 'submit' 
}: ReCAPTCHAProps) {
  const [isReady, setIsReady] = useState(false);
  const widgetRef = useRef<number | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.grecaptcha) {
      setIsReady(true);
    }

    window.onRecaptchaLoad = () => {
      setIsReady(true);
    };

    return () => {
      if (widgetRef.current !== null && window.grecaptcha) {
        window.grecaptcha.reset(widgetRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (isReady && window.grecaptcha) {
      executeRecaptcha();
    }
  }, [isReady, action]);

  const executeRecaptcha = async () => {
    try {
      const token = await window.grecaptcha.execute(siteKey, { action });
      onChange(token);
    } catch (error) {
      console.error('reCAPTCHA error:', error);
      onError?.(error as Error);
    }
  };

  return (
    <>
      <Script
        src={`https://www.google.com/recaptcha/api.js?render=${siteKey}&onload=onRecaptchaLoad`}
        strategy="afterInteractive"
      />
      {/* Invisible reCAPTCHA v3 - no UI element needed */}
    </>
  );
}

/**
 * Hook for form rate limiting
 */
export function useRateLimit(
  identifier: string,
  config: { max: number; window: string }
) {
  const [attempts, setAttempts] = useState(0);
  const [resetAt, setResetAt] = useState<Date | null>(null);

  const checkLimit = async (): Promise<boolean> => {
    const storageKey = `ratelimit:${identifier}`;
    const now = Date.now();
    
    try {
      const stored = localStorage.getItem(storageKey);
      const data = stored ? JSON.parse(stored) : { count: 0, resetAt: 0 };
      
      // Parse window (e.g., '10m' -> 600000ms)
      const windowMs = parseWindow(config.window);
      
      if (now > data.resetAt) {
        data.count = 0;
        data.resetAt = now + windowMs;
      }
      
      if (data.count >= config.max) {
        setAttempts(data.count);
        setResetAt(new Date(data.resetAt));
        return false;
      }
      
      data.count++;
      localStorage.setItem(storageKey, JSON.stringify(data));
      setAttempts(data.count);
      
      return true;
    } catch {
      // If localStorage fails, allow the request
      return true;
    }
  };

  const remaining = Math.max(0, config.max - attempts);
  const resetIn = resetAt ? Math.max(0, resetAt.getTime() - Date.now()) : 0;

  return { checkLimit, remaining, resetIn, resetAt };
}

/**
 * Honeypot field component for bot detection
 */
export function HoneypotField() {
  return (
    <div style={{ position: 'absolute', left: '-9999px' }} aria-hidden="true">
      <input
        type="text"
        name="website"
        tabIndex={-1}
        autoComplete="off"
      />
    </div>
  );
}

/**
 * Secure form wrapper with built-in protections
 */
interface SecureFormProps {
  children: React.ReactNode;
  onSubmit: (data: any) => Promise<void>;
  captchaSiteKey?: string;
  rateLimit?: { max: number; window: string };
  honeypot?: boolean;
}

export function SecureForm({
  children,
  onSubmit,
  captchaSiteKey,
  rateLimit = { max: 3, window: '10m' },
  honeypot = true
}: SecureFormProps) {
  const [captchaToken, setCaptchaToken] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { checkLimit, remaining } = useRateLimit('form-submit', rateLimit);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    // Check honeypot
    if (honeypot) {
      const honeypotField = (e.target as any).website;
      if (honeypotField && honeypotField.value) {
        // Bot detected - fail silently
        return;
      }
    }

    // Check rate limit
    if (!await checkLimit()) {
      setError(`Too many attempts. Please try again later. (${remaining} attempts remaining)`);
      return;
    }

    // Check CAPTCHA
    if (captchaSiteKey && !captchaToken) {
      setError('Please complete the security check');
      return;
    }

    // Get form data
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData);
    
    // Add CAPTCHA token
    if (captchaToken) {
      data.captchaToken = captchaToken;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-4">
          {error}
        </div>
      )}
      
      {children}
      
      {honeypot && <HoneypotField />}
      
      {captchaSiteKey && (
        <ReCAPTCHA
          siteKey={captchaSiteKey}
          onChange={setCaptchaToken}
          onError={(err) => setError(err.message)}
        />
      )}
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 bg-blue-600 text-white hover:bg-blue-700 transition-all disabled:bg-gray-200 disabled:text-gray-400"
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}

// Helper function
function parseWindow(window: string): number {
  const match = window.match(/^(\d+)([smhd])$/);
  if (!match) return 600000; // Default 10 minutes
  
  const [, num, unit] = match;
  const multipliers = { s: 1000, m: 60000, h: 3600000, d: 86400000 };
  
  return parseInt(num) * multipliers[unit as keyof typeof multipliers];
}
