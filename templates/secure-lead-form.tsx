import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button-component';
import { Card } from '@/components/ui/card-component';
import { SecureFormHandler } from '@/lib/forms/secure-form-handler';
import { PIIDetector } from '@/lib/security/pii-detector';

// Auto-generated from field-registry
const formSchema = z.object({
  // Contact Information
  first_name: z.string().min(2, 'First name is required'),
  last_name: z.string().min(2, 'Last name is required'),
  email: z.string().email('Valid email required'),
  phone: z.string().regex(/^\d{10}$/, 'Phone must be 10 digits'),
  zip_code: z.string().regex(/^\d{5}(-\d{4})?$/, 'Valid ZIP code required'),
  
  // Vertical-specific fields
  enrolled_debt_amount: z.number().min(5000).max(1000000),
  employment_status: z.enum(['employed', 'self_employed', 'unemployed', 'retired']),
  
  // Consent
  consent_tcpa: z.boolean().refine(val => val === true, {
    message: 'You must agree to be contacted'
  }),
});

type FormData = z.infer<typeof formSchema>;

export function SecureLeadForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      consent_tcpa: false,
    }
  });

  // Auto-capture tracking parameters on mount
  useEffect(() => {
    // Parse URL for whitelisted params only
    const params = SecureFormHandler.parseSecureParams(
      new URL(window.location.href)
    );
    
    // These are hidden fields, auto-populated from URL
    // NEVER put PII in URLs
    Object.entries(params).forEach(([key, value]) => {
      // Only set if field exists in form
      if (form.getValues(key as any) !== undefined) {
        form.setValue(key as any, value);
      }
    });
  }, []);

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    
    try {
      // All sensitive processing happens server-side
      const response = await fetch('/api/forms/submit', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          // Session ID for tracking
          'X-Session-ID': sessionStorage.getItem('session_id') || '',
        },
        body: JSON.stringify({
          formId: 'lead-form',
          data: {
            ...data,
            // Never log PII
            _metadata: PIIDetector.createSafeObject({
              formName: 'lead-form',
              timestamp: new Date().toISOString(),
            })
          }
        }),
      });
      
      if (!response.ok) {
        throw new Error('Submission failed');
      }
      
      // Success - clear form
      form.reset();
      setShowSuccess(true);
      
      // Track conversion (no PII)
      if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('event', 'conversion', {
          send_to: 'CONVERSION_ID',
          value: 1,
          currency: 'USD',
        });
      }
      
    } catch (error) {
      // Error handling - no PII in logs
      console.error('Form submission error:', {
        error: error instanceof Error ? error.message : 'Unknown error',
        formId: 'lead-form',
      });
      
      form.setError('root', {
        message: 'Something went wrong. Please try again.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (showSuccess) {
    return (
      <Card className="max-w-md mx-auto p-8 text-center">
        <h2 className="text-size-2 font-semibold text-gray-900 mb-4">
          Thank You!
        </h2>
        <p className="text-size-3 text-gray-600">
          We've received your information and will contact you soon.
        </p>
      </Card>
    );
  }

  return (
    <Card className="max-w-md mx-auto">
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <h2 className="text-size-2 font-semibold text-gray-900 mb-6">
          Get Help With Your Debt
        </h2>
        
        {/* Name Fields */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-size-3 font-semibold text-gray-700 block mb-2">
              First Name
            </label>
            <input
              {...form.register('first_name')}
              className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
              autoComplete="given-name"
            />
            {form.formState.errors.first_name && (
              <p className="text-size-4 text-red-600 mt-1">
                {form.formState.errors.first_name.message}
              </p>
            )}
          </div>
          
          <div>
            <label className="text-size-3 font-semibold text-gray-700 block mb-2">
              Last Name
            </label>
            <input
              {...form.register('last_name')}
              className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
              autoComplete="family-name"
            />
            {form.formState.errors.last_name && (
              <p className="text-size-4 text-red-600 mt-1">
                {form.formState.errors.last_name.message}
              </p>
            )}
          </div>
        </div>
        
        {/* Email - Never prepopulate */}
        <div>
          <label className="text-size-3 font-semibold text-gray-700 block mb-2">
            Email Address
          </label>
          <input
            {...form.register('email')}
            type="email"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            autoComplete="email"
          />
          {form.formState.errors.email && (
            <p className="text-size-4 text-red-600 mt-1">
              {form.formState.errors.email.message}
            </p>
          )}
        </div>
        
        {/* Phone - Masked input */}
        <div>
          <label className="text-size-3 font-semibold text-gray-700 block mb-2">
            Phone Number
          </label>
          <input
            {...form.register('phone')}
            type="tel"
            placeholder="(555) 123-4567"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            autoComplete="tel"
          />
          {form.formState.errors.phone && (
            <p className="text-size-4 text-red-600 mt-1">
              {form.formState.errors.phone.message}
            </p>
          )}
        </div>
        
        {/* ZIP Code */}
        <div>
          <label className="text-size-3 font-semibold text-gray-700 block mb-2">
            ZIP Code
          </label>
          <input
            {...form.register('zip_code')}
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            autoComplete="postal-code"
            maxLength={10}
          />
          {form.formState.errors.zip_code && (
            <p className="text-size-4 text-red-600 mt-1">
              {form.formState.errors.zip_code.message}
            </p>
          )}
        </div>
        
        {/* Debt Amount - Sensitive field */}
        <div>
          <label className="text-size-3 font-semibold text-gray-700 block mb-2">
            Total Debt Amount
          </label>
          <input
            {...form.register('enrolled_debt_amount', { 
              valueAsNumber: true 
            })}
            type="number"
            min="5000"
            max="1000000"
            step="100"
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            placeholder="$10,000"
          />
          {form.formState.errors.enrolled_debt_amount && (
            <p className="text-size-4 text-red-600 mt-1">
              {form.formState.errors.enrolled_debt_amount.message}
            </p>
          )}
        </div>
        
        {/* Employment Status */}
        <div>
          <label className="text-size-3 font-semibold text-gray-700 block mb-2">
            Employment Status
          </label>
          <select
            {...form.register('employment_status')}
            className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          >
            <option value="">Select...</option>
            <option value="employed">Employed</option>
            <option value="self_employed">Self Employed</option>
            <option value="unemployed">Unemployed</option>
            <option value="retired">Retired</option>
          </select>
          {form.formState.errors.employment_status && (
            <p className="text-size-4 text-red-600 mt-1">
              {form.formState.errors.employment_status.message}
            </p>
          )}
        </div>
        
        {/* TCPA Consent - Required */}
        <div className="border-2 border-gray-200 rounded-xl p-4 bg-gray-50">
          <label className="flex items-start gap-3">
            <input
              {...form.register('consent_tcpa')}
              type="checkbox"
              className="mt-1 w-5 h-5 rounded border-2 border-gray-300"
            />
            <span className="text-size-4 text-gray-600">
              By checking this box, I agree to receive calls and texts at the 
              number provided, including from auto-dialers. Consent is not 
              required for purchase. Message and data rates may apply.
            </span>
          </label>
          {form.formState.errors.consent_tcpa && (
            <p className="text-size-4 text-red-600 mt-2">
              {form.formState.errors.consent_tcpa.message}
            </p>
          )}
        </div>
        
        {/* Submit Button */}
        <Button
          type="submit"
          variant="primary"
          disabled={isSubmitting}
          loading={isSubmitting}
          className="w-full"
        >
          {isSubmitting ? 'Submitting...' : 'Get Free Consultation'}
        </Button>
        
        {/* Error Display */}
        {form.formState.errors.root && (
          <p className="text-size-3 text-red-600 text-center">
            {form.formState.errors.root.message}
          </p>
        )}
        
        {/* Privacy Note */}
        <p className="text-size-4 text-gray-500 text-center">
          Your information is secure and will never be sold. 
          View our <a href="/privacy" className="underline">Privacy Policy</a>.
        </p>
      </form>
    </Card>
  );
}
