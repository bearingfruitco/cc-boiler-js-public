/**
 * TCPA-compliant Lead Form Component
 * Automatically handles TrustedForm and Jornaya integration
 */

import { useRef } from 'react';
import { useTCPA } from '@/hooks/use-tcpa';
import { SecureLeadForm } from '@/templates/secure-lead-form';
import type { TCPAFormData } from '@/lib/tcpa/types';

interface TCPALeadFormProps {
  onSubmit?: (data: any) => Promise<void>;
  className?: string;
}

export function TCPALeadForm({ onSubmit, className }: TCPALeadFormProps) {
  const formRef = useRef<HTMLFormElement>(null);
  const { 
    initialized, 
    enabled, 
    providers,
    getTCPAData,
    validateCompliance,
    storeTCPAData 
  } = useTCPA({ 
    autoInject: true,
    formRef 
  });
  
  const handleSubmit = async (formData: any) => {
    try {
      // Add TCPA data if enabled
      let enhancedData = formData;
      
      if (enabled) {
        // Get TCPA certificates/tokens
        const tcpaData = await getTCPAData();
        enhancedData = { ...formData, ...tcpaData };
        
        // Validate compliance
        const compliance = await validateCompliance(enhancedData);
        if (!compliance.valid) {
          console.error('[TCPA] Compliance validation failed:', compliance.errors);
          // You might want to show these errors to the user
          throw new Error(compliance.errors.join(', '));
        }
        
        // Store TCPA data after successful submission
        // Note: In real implementation, leadId would come from the API response
        const leadId = `lead_${Date.now()}`;
        await storeTCPAData(leadId, tcpaData as TCPAFormData);
      }
      
      // Call original submit handler
      if (onSubmit) {
        await onSubmit(enhancedData);
      }
    } catch (error) {
      console.error('[TCPALeadForm] Submission error:', error);
      throw error;
    }
  };
  
  return (
    <div className={className}>
      {/* Show TCPA status in development */}
      {process.env.NODE_ENV === 'development' && enabled && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-size-4">
          <p className="font-semibold text-blue-900">TCPA Compliance Active</p>
          <p className="text-blue-700">Providers: {providers.join(', ')}</p>
        </div>
      )}
      
      {/* Hidden fields for TCPA */}
      {enabled && (
        <>
          <input type="hidden" id="xxTrustedFormCertUrl" name="xxTrustedFormCertUrl" />
          <input type="hidden" id="xxTrustedFormPingUrl" name="xxTrustedFormPingUrl" />
          <input type="hidden" id="leadid_token" name="leadid_token" />
        </>
      )}
      
      {/* Render the secure form */}
      <form ref={formRef}>
        <SecureLeadForm onSubmit={handleSubmit} />
      </form>
      
      {/* Jornaya noscript fallback */}
      {enabled && providers.includes('jornaya') && (
        <noscript>
          <img src="//create.leadid.com/?.gif?o=1" 
               width="1" height="1" alt="" />
        </noscript>
      )}
    </div>
  );
}
