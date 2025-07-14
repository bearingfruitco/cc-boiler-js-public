/**
 * React hook for TCPA compliance
 */

import { useEffect, useState, useRef } from 'react';
import { getTCPAManager } from '@/lib/tcpa';
import type { TCPAFormData } from '@/lib/tcpa/types';

interface UseTCPAOptions {
  autoInject?: boolean;
  formRef?: React.RefObject<HTMLFormElement>;
}

interface UseTCPAReturn {
  initialized: boolean;
  enabled: boolean;
  providers: string[];
  injectScripts: () => Promise<void>;
  prepareForm: (form: HTMLFormElement) => void;
  getTCPAData: () => Promise<TCPAFormData>;
  validateCompliance: (formData: any) => Promise<{ valid: boolean; errors: string[] }>;
  storeTCPAData: (leadId: string, formData: TCPAFormData) => Promise<void>;
}

export function useTCPA(options: UseTCPAOptions = {}): UseTCPAReturn {
  const [initialized, setInitialized] = useState(false);
  const [enabled, setEnabled] = useState(false);
  const [providers, setProviders] = useState<string[]>([]);
  const managerRef = useRef<any>(null);
  
  useEffect(() => {
    async function init() {
      const manager = await getTCPAManager();
      if (!manager) {
        setEnabled(false);
        setInitialized(true);
        return;
      }
      
      managerRef.current = manager;
      await manager.initialize();
      
      setEnabled(manager.isEnabled());
      setProviders(manager.getEnabledProviders());
      setInitialized(true);
      
      // Auto-inject scripts if requested
      if (options.autoInject && manager.isEnabled()) {
        await manager.injectScripts();
      }
      
      // Prepare form if ref provided
      if (options.formRef?.current && manager.isEnabled()) {
        manager.prepareForm(options.formRef.current);
      }
    }
    
    init();
  }, [options.autoInject]);
  
  // Prepare form when ref changes
  useEffect(() => {
    if (initialized && enabled && options.formRef?.current && managerRef.current) {
      managerRef.current.prepareForm(options.formRef.current);
    }
  }, [initialized, enabled, options.formRef?.current]);
  
  return {
    initialized,
    enabled,
    providers,
    injectScripts: async () => {
      if (managerRef.current) {
        await managerRef.current.injectScripts();
      }
    },
    prepareForm: (form: HTMLFormElement) => {
      if (managerRef.current) {
        managerRef.current.prepareForm(form);
      }
    },
    getTCPAData: async () => {
      if (managerRef.current) {
        return await managerRef.current.getTCPAData();
      }
      return {};
    },
    validateCompliance: async (formData: any) => {
      if (managerRef.current) {
        return await managerRef.current.validateCompliance(formData);
      }
      return { valid: true, errors: [] };
    },
    storeTCPAData: async (leadId: string, formData: TCPAFormData) => {
      if (managerRef.current) {
        await managerRef.current.storeTCPAData(leadId, formData);
      }
    }
  };
}
