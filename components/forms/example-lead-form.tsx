// components/forms/example-lead-form.tsx
'use client';

import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useFormStore } from '@/stores/form-store';
import { useCreateLead } from '@/hooks/mutations';
import { useLeadFormEvents } from '@/hooks/use-event-system';
import { ChevronRight, AlertCircle } from 'lucide-react';

// Validation schema
const leadFormSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  phone: z.string().regex(/^\d{10}$/, 'Phone must be 10 digits'),
  debtAmount: z.number().min(1000, 'Minimum debt amount is $1,000').max(1000000),
  state: z.string().length(2, 'Please select a state'),
  debtTypes: z.array(z.string()).min(1, 'Select at least one debt type'),
  agreeToTerms: z.boolean().refine(val => val === true, 'You must agree to the terms'),
});

type LeadFormData = z.infer<typeof leadFormSchema>;

export function ExampleLeadForm() {
  // Form store
  const { 
    formData, 
    updateFormField, 
    updateMultipleFields, 
    trackFieldInteraction,
    setSubmitting,
    isSubmitting 
  } = useFormStore();
  
  // Event tracking
  const {
    trackFormStart,
    trackFieldChange,
    trackFormSubmit,
    trackSubmissionResult
  } = useLeadFormEvents('example-lead-form');
  
  // Mutation hook
  const { mutate: createLead, isLoading: isCreating, error: submitError } = useCreateLead();
  
  // React Hook Form
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<LeadFormData>({
    resolver: zodResolver(leadFormSchema),
    defaultValues: {
      name: formData.name || '',
      email: formData.email || '',
      phone: formData.phone || '',
      debtAmount: formData.debtAmount || undefined,
      state: formData.state || '',
      debtTypes: formData.debtTypes || [],
      agreeToTerms: formData.agreeToTerms || false,
    },
  });
  
  // Track form start on first interaction
  useEffect(() => {
    const handleFirstInteraction = () => {
      trackFormStart();
      document.removeEventListener('click', handleFirstInteraction);
      document.removeEventListener('focus', handleFirstInteraction, true);
    };
    
    document.addEventListener('click', handleFirstInteraction);
    document.addEventListener('focus', handleFirstInteraction, true);
    
    return () => {
      document.removeEventListener('click', handleFirstInteraction);
      document.removeEventListener('focus', handleFirstInteraction, true);
    };
  }, [trackFormStart]);
  
  // Sync form changes to store and track changes
  useEffect(() => {
    const subscription = watch((value, { name, type }) => {
      if (name && type === 'change') {
        const fieldValue = value[name as keyof LeadFormData];
        const oldValue = formData[name];
        
        updateFormField(name, fieldValue);
        trackFieldChange(name, oldValue, fieldValue, !errors[name as keyof LeadFormData]);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch, updateFormField, trackFieldChange, formData, errors]);
  
  // Calculate completion percentage
  const calculateCompletion = () => {
    const fields = ['name', 'email', 'phone', 'debtAmount', 'state', 'debtTypes', 'agreeToTerms'];
    const completed = fields.filter(field => {
      const value = formData[field];
      if (field === 'debtTypes') return Array.isArray(value) && value.length > 0;
      if (field === 'agreeToTerms') return value === true;
      return value && value !== '';
    }).length;
    return (completed / fields.length) * 100;
  };
  
  // Handle form submission
  const onSubmit = async (data: LeadFormData) => {
    const startTime = await trackFormSubmit(data);
    setSubmitting(true);
    
    try {
      // Update store with final data
      updateMultipleFields(data);
      
      // Submit via mutation
      const result = await createLead(data);
      
      // Track success
      trackSubmissionResult(true, startTime);
      
      // Redirect on success
      if (result?.id) {
        window.location.href = `/thank-you?id=${result.id}`;
      }
    } catch (error) {
      console.error('Form submission error:', error);
      trackSubmissionResult(false, startTime, {
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    } finally {
      setSubmitting(false);
    }
  };
  
  const debtTypes = [
    { value: 'credit_card', label: 'Credit Cards' },
    { value: 'medical', label: 'Medical Bills' },
    { value: 'personal_loan', label: 'Personal Loans' },
    { value: 'student_loan', label: 'Student Loans' },
    { value: 'other', label: 'Other' },
  ];
  
  const completionPercentage = calculateCompletion();
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between text-size-4 text-gray-600 mb-2">
          <span>Form Progress</span>
          <span>{Math.round(completionPercentage)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${completionPercentage}%` }}
          />
        </div>
      </div>
      
      {/* Name Field */}
      <div className="space-y-2">
        <label htmlFor="name" className="text-size-3 font-semibold text-gray-700">
          Full Name
        </label>
        <input
          {...register('name')}
          id="name"
          type="text"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          placeholder="John Doe"
          onFocus={() => trackFieldInteraction('name', 'focus')}
          onBlur={() => trackFieldInteraction('name', 'blur')}
        />
        {errors.name && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.name.message}
          </p>
        )}
      </div>
      
      {/* Email Field */}
      <div className="space-y-2">
        <label htmlFor="email" className="text-size-3 font-semibold text-gray-700">
          Email Address
        </label>
        <input
          {...register('email')}
          id="email"
          type="email"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          placeholder="john@example.com"
          onFocus={() => trackFieldInteraction('email', 'focus')}
          onBlur={() => trackFieldInteraction('email', 'blur')}
        />
        {errors.email && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.email.message}
          </p>
        )}
      </div>
      
      {/* Phone Field */}
      <div className="space-y-2">
        <label htmlFor="phone" className="text-size-3 font-semibold text-gray-700">
          Phone Number
        </label>
        <input
          {...register('phone')}
          id="phone"
          type="tel"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          placeholder="5551234567"
          onFocus={() => trackFieldInteraction('phone', 'focus')}
          onBlur={() => trackFieldInteraction('phone', 'blur')}
        />
        {errors.phone && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.phone.message}
          </p>
        )}
      </div>
      
      {/* Debt Amount Field */}
      <div className="space-y-2">
        <label htmlFor="debtAmount" className="text-size-3 font-semibold text-gray-700">
          Total Debt Amount
        </label>
        <div className="relative">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">$</span>
          <input
            {...register('debtAmount', { valueAsNumber: true })}
            id="debtAmount"
            type="number"
            className="w-full h-12 pl-8 pr-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
            placeholder="25000"
            onFocus={() => trackFieldInteraction('debtAmount', 'focus')}
            onBlur={() => trackFieldInteraction('debtAmount', 'blur')}
          />
        </div>
        {errors.debtAmount && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.debtAmount.message}
          </p>
        )}
      </div>
      
      {/* State Field */}
      <div className="space-y-2">
        <label htmlFor="state" className="text-size-3 font-semibold text-gray-700">
          State
        </label>
        <select
          {...register('state')}
          id="state"
          className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          onFocus={() => trackFieldInteraction('state', 'focus')}
          onBlur={() => trackFieldInteraction('state', 'blur')}
        >
          <option value="">Select your state</option>
          <option value="CA">California</option>
          <option value="TX">Texas</option>
          <option value="FL">Florida</option>
          <option value="NY">New York</option>
          {/* Add more states */}
        </select>
        {errors.state && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.state.message}
          </p>
        )}
      </div>
      
      {/* Debt Types Field */}
      <div className="space-y-2">
        <label className="text-size-3 font-semibold text-gray-700">
          Types of Debt (Select all that apply)
        </label>
        <div className="space-y-3">
          {debtTypes.map((type) => (
            <label key={type.value} className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                value={type.value}
                {...register('debtTypes')}
                className="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
                onChange={() => trackFieldInteraction('debtTypes', 'change')}
              />
              <span className="text-size-3 text-gray-700">{type.label}</span>
            </label>
          ))}
        </div>
        {errors.debtTypes && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.debtTypes.message}
          </p>
        )}
      </div>
      
      {/* Terms Agreement */}
      <div className="space-y-2">
        <label className="flex items-start gap-3 cursor-pointer">
          <input
            {...register('agreeToTerms')}
            type="checkbox"
            className="w-5 h-5 mt-1 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500"
            onChange={() => trackFieldInteraction('agreeToTerms', 'change')}
          />
          <span className="text-size-4 text-gray-600">
            By submitting this form, I agree to be contacted by FreshSlate and its partners
            regarding debt relief options. I understand that consent is not required for purchase.
          </span>
        </label>
        {errors.agreeToTerms && (
          <p className="text-size-4 text-red-600 flex items-center gap-1">
            <AlertCircle className="w-4 h-4" />
            {errors.agreeToTerms.message}
          </p>
        )}
      </div>
      
      {/* Submit Error */}
      {submitError && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-size-3 text-red-700">
            {submitError instanceof Error ? submitError.message : 'Failed to submit form. Please try again.'}
          </p>
        </div>
      )}
      
      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting || isCreating}
        className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-200 disabled:text-gray-400 transition-all flex items-center justify-center gap-2"
      >
        {isSubmitting || isCreating ? (
          'Submitting...'
        ) : (
          <>
            Get Your Free Consultation
            <ChevronRight className="w-5 h-5" />
          </>
        )}
      </button>
    </form>
  );
}
