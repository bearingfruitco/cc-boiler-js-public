'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { SecureForm, ReCAPTCHA, useRateLimit } from '@/components/security/captcha';
import { Button } from '@/components/ui/button';
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

/**
 * Secure Form Component Template
 * Includes CAPTCHA, rate limiting, validation, and tracking
 */

// Form validation schema
const formSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),
  email: z.string()
    .email('Please enter a valid email'),
  phone: z.string()
    .regex(/^\d{10}$/, 'Phone must be 10 digits')
    .optional(),
  message: z.string()
    .min(10, 'Message must be at least 10 characters')
    .max(500, 'Message must be less than 500 characters'),
  consent: z.boolean()
    .refine(val => val === true, 'You must agree to the terms'),
});

type FormData = z.infer<typeof formSchema>;

interface SecureContactFormProps {
  onSuccess?: () => void;
  captchaSiteKey?: string;
}

export function SecureContactForm({ 
  onSuccess,
  captchaSiteKey = process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY 
}: SecureContactFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [captchaToken, setCaptchaToken] = useState('');
  
  // Rate limiting
  const { checkLimit, remaining } = useRateLimit('contact-form', {
    max: 3,
    window: '10m'
  });
  
  // React Hook Form
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      consent: false
    }
  });
  
  // Track form engagement
  const watchedFields = watch();
  useState(() => {
    // Track form view
    eventQueue.emit(LEAD_EVENTS.FORM_VIEWED, {
      formName: 'secure-contact',
      timestamp: Date.now()
    });
  });
  
  const onSubmit = async (data: FormData) => {
    setSubmitError('');
    setSubmitSuccess(false);
    
    // Check rate limit
    if (!await checkLimit()) {
      setSubmitError(`Too many attempts. Please try again later. (${remaining} attempts remaining)`);
      return;
    }
    
    // Verify CAPTCHA
    if (captchaSiteKey && !captchaToken) {
      setSubmitError('Please complete the security check');
      return;
    }
    
    setIsSubmitting(true);
    
    // Track submission attempt
    eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
      formName: 'secure-contact',
      hasConsent: data.consent,
      timestamp: Date.now()
    });
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...data,
          captchaToken,
          source: 'secure-contact-form',
          timestamp: new Date().toISOString()
        }),
      });
      
      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || 'Failed to submit form');
      }
      
      // Track successful submission
      eventQueue.emit(LEAD_EVENTS.LEAD_CAPTURED, {
        formName: 'secure-contact',
        leadId: result.leadId,
        timestamp: Date.now()
      });
      
      setSubmitSuccess(true);
      reset();
      onSuccess?.();
      
    } catch (error) {
      console.error('Form submission error:', error);
      setSubmitError(error instanceof Error ? error.message : 'Something went wrong');
      
      // Track error
      eventQueue.emit(LEAD_EVENTS.FORM_ERROR, {
        formName: 'secure-contact',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: Date.now()
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Success Message */}
        {submitSuccess && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-xl">
            Thank you! Your message has been sent successfully.
          </div>
        )}
        
        {/* Error Message */}
        {submitError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
            {submitError}
          </div>
        )}
        
        {/* Name Field */}
        <div className="space-y-2">
          <label htmlFor="name" className="text-size-3 font-semibold text-gray-700">
            Name *
          </label>
          <input
            {...register('name')}
            id="name"
            type="text"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            placeholder="Your name"
          />
          {errors.name && (
            <p className="text-size-4 text-red-600">{errors.name.message}</p>
          )}
        </div>
        
        {/* Email Field */}
        <div className="space-y-2">
          <label htmlFor="email" className="text-size-3 font-semibold text-gray-700">
            Email *
          </label>
          <input
            {...register('email')}
            id="email"
            type="email"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            placeholder="your.email@example.com"
          />
          {errors.email && (
            <p className="text-size-4 text-red-600">{errors.email.message}</p>
          )}
        </div>
        
        {/* Phone Field (Optional) */}
        <div className="space-y-2">
          <label htmlFor="phone" className="text-size-3 font-semibold text-gray-700">
            Phone
          </label>
          <input
            {...register('phone')}
            id="phone"
            type="tel"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            placeholder="1234567890"
          />
          {errors.phone && (
            <p className="text-size-4 text-red-600">{errors.phone.message}</p>
          )}
        </div>
        
        {/* Message Field */}
        <div className="space-y-2">
          <label htmlFor="message" className="text-size-3 font-semibold text-gray-700">
            Message *
          </label>
          <textarea
            {...register('message')}
            id="message"
            rows={4}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors resize-none"
            placeholder="How can we help you?"
          />
          {errors.message && (
            <p className="text-size-4 text-red-600">{errors.message.message}</p>
          )}
        </div>
        
        {/* Consent Checkbox */}
        <div className="space-y-2">
          <label className="flex items-start gap-3">
            <input
              {...register('consent')}
              type="checkbox"
              className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span className="text-size-4 text-gray-600">
              I agree to the terms and conditions and understand my information will be used as described in the privacy policy. *
            </span>
          </label>
          {errors.consent && (
            <p className="text-size-4 text-red-600">{errors.consent.message}</p>
          )}
        </div>
        
        {/* CAPTCHA */}
        {captchaSiteKey && (
          <ReCAPTCHA
            siteKey={captchaSiteKey}
            onChange={setCaptchaToken}
            onError={(error) => setSubmitError(error.message)}
          />
        )}
        
        {/* Honeypot (invisible) */}
        <div style={{ position: 'absolute', left: '-9999px' }} aria-hidden="true">
          <input
            type="text"
            name="website"
            tabIndex={-1}
            autoComplete="off"
          />
        </div>
        
        {/* Submit Button */}
        <Button
          type="submit"
          loading={isSubmitting}
          disabled={isSubmitting || submitSuccess}
          fullWidth
        >
          {isSubmitting ? 'Sending...' : 'Send Message'}
        </Button>
        
        {/* Rate Limit Info */}
        {remaining < 3 && remaining > 0 && (
          <p className="text-size-4 text-gray-500 text-center">
            {remaining} submission{remaining !== 1 ? 's' : ''} remaining
          </p>
        )}
      </form>
    </div>
  );
}

// Export a wrapped version with default security settings
export function ContactForm(props: Omit<SecureContactFormProps, 'captchaSiteKey'>) {
  return (
    <SecureContactForm
      {...props}
      captchaSiteKey={process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}
    />
  );
}
