/**
 * Jornaya Provider for TCPA Compliance
 * Handles LeadiD token generation and validation
 */

import type { TCPAConfig } from './types';

export class JornayaProvider {
  private static instance: JornayaProvider;
  private config: TCPAConfig['providers']['jornaya'];
  private scriptLoaded = false;
  
  constructor(config: TCPAConfig['providers']['jornaya']) {
    this.config = config;
  }
  
  static getInstance(config?: TCPAConfig['providers']['jornaya']): JornayaProvider | null {
    if (!config?.enabled) return null;
    
    if (!this.instance && config) {
      this.instance = new JornayaProvider(config);
    }
    return this.instance;
  }
  
  /**
   * Inject Jornaya LeadiD script
   */
  async injectScript(): Promise<void> {
    if (!this.config.enabled || this.scriptLoaded) return;
    
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.id = 'LeadiDscript';
      script.type = 'text/javascript';
      script.async = true;
      script.src = `${this.config.scriptUrl}${this.config.campaignId}.js?snippet_version=2`;
      
      script.onload = () => {
        this.scriptLoaded = true;
        console.log('[Jornaya] LeadiD script loaded successfully');
        
        // Wait for LeadiD to be available
        let attempts = 0;
        const checkInterval = setInterval(() => {
          if ((window as any).LeadiD || attempts > 20) {
            clearInterval(checkInterval);
            resolve();
          }
          attempts++;
        }, 100);
      };
      
      script.onerror = () => {
        console.error('[Jornaya] Failed to load LeadiD script');
        reject(new Error('Failed to load Jornaya script'));
      };
      
      document.body.appendChild(script);
    });
  }
  
  /**
   * Get LeadiD token
   */
  getLeadId(): string | null {
    if (!this.config.enabled) return null;
    
    // Check window.LeadiD
    if (typeof window !== 'undefined' && (window as any).LeadiD) {
      return (window as any).LeadiD.token || null;
    }
    
    // Check hidden field as fallback
    const leadIdField = document.getElementById('leadid_token') as HTMLInputElement;
    return leadIdField?.value || null;
  }
  
  /**
   * Get LeadiD URL (for iframe implementations)
   */
  getLeadIdUrl(): string | null {
    if (!this.config.enabled) return null;
    
    if (typeof window !== 'undefined' && (window as any).LeadiD) {
      return (window as any).LeadiD.url || null;
    }
    
    return null;
  }
  
  /**
   * Validate token with Jornaya API
   */
  async validateToken(token: string): Promise<{
    valid: boolean;
    data?: any;
    error?: string;
  }> {
    try {
      const response = await fetch('/api/tcpa/verify-jornaya', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          token,
          accountId: this.config.accountId 
        })
      });
      
      if (!response.ok) {
        const error = await response.text();
        return { valid: false, error };
      }
      
      const data = await response.json();
      return { valid: true, data };
    } catch (error) {
      console.error('[Jornaya] Token validation failed:', error);
      return { 
        valid: false, 
        error: error instanceof Error ? error.message : 'Validation failed' 
      };
    }
  }
  
  /**
   * Store LeadiD for audit trail
   */
  async storeLeadId(leadId: string, token: string, additionalData?: any): Promise<void> {
    try {
      await fetch('/api/tcpa/store-certificate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          leadId,
          certUrl: token, // Store token as certUrl for consistency
          certType: 'jornaya',
          retentionDays: 90, // Default retention
          additionalData
        })
      });
    } catch (error) {
      console.error('[Jornaya] Failed to store LeadiD:', error);
      throw error;
    }
  }
  
  /**
   * Add hidden field to form
   */
  addHiddenField(formElement: HTMLFormElement): void {
    if (!this.config.enabled) return;
    
    // Check if field already exists
    if (formElement.querySelector('#leadid_token')) return;
    
    const leadIdField = document.createElement('input');
    leadIdField.type = 'hidden';
    leadIdField.id = 'leadid_token';
    leadIdField.name = 'leadid_token';
    formElement.appendChild(leadIdField);
  }
  
  /**
   * Create noscript iframe fallback
   */
  createNoScriptFallback(): string {
    if (!this.config.enabled) return '';
    
    return `<noscript>
      <img src="//create.leadid.com/${this.config.campaignId}.gif?o=1" 
           width="1" height="1" alt="" />
    </noscript>`;
  }
}
