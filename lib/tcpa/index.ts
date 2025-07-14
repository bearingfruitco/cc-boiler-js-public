/**
 * TCPA Manager - Central orchestrator for TCPA compliance
 */

import { TrustedFormProvider } from './trustedform-provider';
import { JornayaProvider } from './jornaya-provider';
import type { TCPAConfig, TCPAFormData } from './types';

export class TCPAManager {
  private static instance: TCPAManager;
  private config: TCPAConfig;
  private trustedForm: TrustedFormProvider | null = null;
  private jornaya: JornayaProvider | null = null;
  private initialized = false;
  
  constructor(config: TCPAConfig) {
    this.config = config;
  }
  
  static async getInstance(): Promise<TCPAManager | null> {
    if (!this.instance) {
      // Load config
      const config = await this.loadConfig();
      if (!config?.enabled) return null;
      
      this.instance = new TCPAManager(config);
    }
    return this.instance;
  }
  
  /**
   * Load TCPA configuration
   */
  private static async loadConfig(): Promise<TCPAConfig | null> {
    try {
      const response = await fetch('/.claude/tcpa.config.json');
      if (!response.ok) return null;
      return await response.json();
    } catch {
      // Config doesn't exist or is disabled
      return null;
    }
  }
  
  /**
   * Initialize TCPA providers
   */
  async initialize(): Promise<void> {
    if (this.initialized || !this.config.enabled) return;
    
    // Initialize providers
    this.trustedForm = TrustedFormProvider.getInstance(this.config.providers.trustedform);
    this.jornaya = JornayaProvider.getInstance(this.config.providers.jornaya);
    
    // Auto-inject scripts if enabled
    if (this.config.features.autoInjectScripts) {
      await this.injectScripts();
    }
    
    this.initialized = true;
  }
  
  /**
   * Inject all enabled provider scripts
   */
  async injectScripts(): Promise<void> {
    const promises = [];
    
    if (this.trustedForm) {
      promises.push(this.trustedForm.injectScript());
    }
    
    if (this.jornaya) {
      promises.push(this.jornaya.injectScript());
    }
    
    await Promise.allSettled(promises);
  }
  
  /**
   * Prepare form for TCPA compliance
   */
  prepareForm(formElement: HTMLFormElement): void {
    if (!this.initialized || !this.config.enabled) return;
    
    // Add hidden fields
    this.trustedForm?.addHiddenFields(formElement);
    this.jornaya?.addHiddenField(formElement);
    
    // Add consent checkbox if missing
    if (this.config.compliance.requireConsent) {
      this.ensureConsentField(formElement);
    }
  }
  
  /**
   * Get TCPA data for form submission
   */
  async getTCPAData(): Promise<TCPAFormData> {
    const data: TCPAFormData = {
      tcpa_timestamp: new Date().toISOString(),
    };
    
    // Get certificates/tokens
    if (this.trustedForm) {
      data.trustedform_cert = this.trustedForm.getCertificate() || undefined;
    }
    
    if (this.jornaya) {
      data.jornaya_leadid = this.jornaya.getLeadId() || undefined;
    }
    
    // Get IP address
    try {
      const response = await fetch('/api/client-ip');
      if (response.ok) {
        data.tcpa_ip = await response.text();
      }
    } catch {
      // IP fetch failed, continue without it
    }
    
    return data;
  }
  
  /**
   * Validate TCPA compliance
   */
  async validateCompliance(formData: any): Promise<{
    valid: boolean;
    errors: string[];
  }> {
    const errors: string[] = [];
    
    // Check consent
    if (this.config.compliance.requireConsent && !formData.consent_tcpa) {
      errors.push('TCPA consent is required');
    }
    
    // Check certificates if required
    if (this.config.compliance.blockSubmissionWithoutCert) {
      if (this.trustedForm && !formData.trustedform_cert) {
        errors.push('TrustedForm certificate is required');
      }
      
      if (this.jornaya && !formData.jornaya_leadid) {
        errors.push('Jornaya LeadiD is required');
      }
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  /**
   * Store certificates and consent
   */
  async storeTCPAData(leadId: string, formData: TCPAFormData): Promise<void> {
    const promises = [];
    
    // Store TrustedForm certificate
    if (this.trustedForm && formData.trustedform_cert) {
      promises.push(
        this.trustedForm.storeCertificate(leadId, formData.trustedform_cert)
      );
    }
    
    // Store Jornaya LeadiD
    if (this.jornaya && formData.jornaya_leadid) {
      promises.push(
        this.jornaya.storeLeadId(leadId, formData.jornaya_leadid)
      );
    }
    
    // Store consent record
    if (formData.consent_tcpa) {
      promises.push(this.storeConsent(leadId, formData));
    }
    
    await Promise.allSettled(promises);
  }
  
  /**
   * Store consent record
   */
  private async storeConsent(leadId: string, formData: TCPAFormData): Promise<void> {
    try {
      await fetch('/api/tcpa/store-consent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          leadId,
          consentText: this.config.compliance.consentLanguage,
          consentedAt: formData.tcpa_timestamp,
          ipAddress: formData.tcpa_ip || 'unknown',
          userAgent: navigator.userAgent,
          pageUrl: window.location.href
        })
      });
    } catch (error) {
      console.error('[TCPA] Failed to store consent:', error);
    }
  }
  
  /**
   * Ensure consent field exists
   */
  private ensureConsentField(formElement: HTMLFormElement): void {
    // Check if consent field exists
    if (formElement.querySelector('[name="consent_tcpa"]')) return;
    
    // Create consent container
    const consentDiv = document.createElement('div');
    consentDiv.className = 'border-2 border-gray-200 rounded-xl p-4 bg-gray-50 mb-4';
    
    const label = document.createElement('label');
    label.className = 'flex items-start gap-3';
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = 'consent_tcpa';
    checkbox.required = true;
    checkbox.className = 'mt-1 w-5 h-5 rounded border-2 border-gray-300';
    
    const text = document.createElement('span');
    text.className = 'text-size-4 text-gray-600';
    text.textContent = this.config.compliance.consentLanguage;
    
    label.appendChild(checkbox);
    label.appendChild(text);
    consentDiv.appendChild(label);
    
    // Insert before submit button
    const submitButton = formElement.querySelector('[type="submit"]');
    if (submitButton) {
      submitButton.parentElement?.insertBefore(consentDiv, submitButton);
    } else {
      formElement.appendChild(consentDiv);
    }
  }
  
  /**
   * Check if TCPA is enabled
   */
  isEnabled(): boolean {
    return this.config.enabled && this.initialized;
  }
  
  /**
   * Get enabled providers
   */
  getEnabledProviders(): string[] {
    const providers = [];
    if (this.trustedForm) providers.push('trustedform');
    if (this.jornaya) providers.push('jornaya');
    return providers;
  }
}

// Export singleton getter
export const getTCPAManager = TCPAManager.getInstance;
