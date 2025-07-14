/**
 * TrustedForm Provider for TCPA Compliance
 * Handles certificate generation, validation, and storage
 */

import type { TCPAConfig } from './types';

export class TrustedFormProvider {
  private static instance: TrustedFormProvider;
  private config: TCPAConfig['providers']['trustedform'];
  private scriptLoaded = false;
  
  constructor(config: TCPAConfig['providers']['trustedform']) {
    this.config = config;
  }
  
  static getInstance(config?: TCPAConfig['providers']['trustedform']): TrustedFormProvider | null {
    if (!config?.enabled) return null;
    
    if (!this.instance && config) {
      this.instance = new TrustedFormProvider(config);
    }
    return this.instance;
  }
  
  /**
   * Inject TrustedForm script into the page
   */
  async injectScript(): Promise<void> {
    if (!this.config.enabled || this.scriptLoaded) return;
    
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.async = true;
      script.src = `${this.config.scriptUrl}?field=xxTrustedFormCertUrl&ping_field=xxTrustedFormPingUrl&l=${this.config.accountId}`;
      
      script.onload = () => {
        this.scriptLoaded = true;
        console.log('[TrustedForm] Script loaded successfully');
        resolve();
      };
      
      script.onerror = () => {
        console.error('[TrustedForm] Failed to load script');
        reject(new Error('Failed to load TrustedForm script'));
      };
      
      const firstScript = document.getElementsByTagName('script')[0];
      firstScript.parentNode?.insertBefore(script, firstScript);
    });
  }
  
  /**
   * Get certificate from hidden form field
   */
  getCertificate(): string | null {
    if (!this.config.enabled) return null;
    
    const certField = document.getElementById('xxTrustedFormCertUrl') as HTMLInputElement;
    return certField?.value || null;
  }
  
  /**
   * Get ping URL from hidden form field
   */
  getPingUrl(): string | null {
    if (!this.config.enabled) return null;
    
    const pingField = document.getElementById('xxTrustedFormPingUrl') as HTMLInputElement;
    return pingField?.value || null;
  }
  
  /**
   * Verify certificate with TrustedForm API
   */
  async verifyCertificate(certUrl: string): Promise<{
    valid: boolean;
    data?: any;
    error?: string;
  }> {
    try {
      const response = await fetch('/api/tcpa/verify-trustedform', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          certUrl,
          apiKey: this.config.apiKey 
        })
      });
      
      if (!response.ok) {
        const error = await response.text();
        return { valid: false, error };
      }
      
      const data = await response.json();
      return { valid: true, data };
    } catch (error) {
      console.error('[TrustedForm] Certificate verification failed:', error);
      return { 
        valid: false, 
        error: error instanceof Error ? error.message : 'Verification failed' 
      };
    }
  }
  
  /**
   * Store certificate for retention period
   */
  async storeCertificate(leadId: string, certUrl: string, additionalData?: any): Promise<void> {
    if (!this.config.retainCerts) return;
    
    try {
      await fetch('/api/tcpa/store-certificate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          leadId,
          certUrl,
          certType: 'trustedform',
          retentionDays: this.config.certRetentionDays,
          additionalData
        })
      });
    } catch (error) {
      console.error('[TrustedForm] Failed to store certificate:', error);
      throw error;
    }
  }
  
  /**
   * Add hidden fields to form
   */
  addHiddenFields(formElement: HTMLFormElement): void {
    if (!this.config.enabled) return;
    
    // Check if fields already exist
    if (formElement.querySelector('#xxTrustedFormCertUrl')) return;
    
    // Certificate URL field
    const certField = document.createElement('input');
    certField.type = 'hidden';
    certField.id = 'xxTrustedFormCertUrl';
    certField.name = 'xxTrustedFormCertUrl';
    formElement.appendChild(certField);
    
    // Ping URL field
    const pingField = document.createElement('input');
    pingField.type = 'hidden';
    pingField.id = 'xxTrustedFormPingUrl';
    pingField.name = 'xxTrustedFormPingUrl';
    formElement.appendChild(pingField);
  }
}
