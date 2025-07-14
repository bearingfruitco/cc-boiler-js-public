/**
 * TCPA Types and Interfaces
 */

export interface TCPAConfig {
  enabled: boolean;
  version: string;
  description: string;
  providers: {
    trustedform: {
      enabled: boolean;
      accountId: string;
      apiKey: string;
      scriptUrl: string;
      retainCerts: boolean;
      certRetentionDays: number;
      autoInject: boolean;
    };
    jornaya: {
      enabled: boolean;
      accountId: string;
      campaignId: string;
      siteId: string;
      scriptUrl: string;
      autoInject: boolean;
    };
  };
  features: {
    autoInjectScripts: boolean;
    certStorage: 'database' | 'filesystem';
    complianceAudit: boolean;
    consentTracking: boolean;
    certVerification: boolean;
    retentionPolicy: boolean;
  };
  storage: {
    certificatesTable: string;
    consentsTable: string;
    verificationsTable: string;
  };
  compliance: {
    requireConsent: boolean;
    consentLanguage: string;
    blockSubmissionWithoutCert: boolean;
    auditLogRetention: number;
  };
}

export interface TCPACertificate {
  id: string;
  leadId: string;
  certUrl: string;
  certType: 'trustedform' | 'jornaya';
  createdAt: Date;
  expiresAt: Date;
  verified: boolean;
  verificationData?: any;
}

export interface TCPAConsent {
  id: string;
  leadId: string;
  consentText: string;
  consentedAt: Date;
  ipAddress: string;
  userAgent: string;
  pageUrl: string;
  certificateId?: string;
}

export interface TCPAVerification {
  id: string;
  certificateId: string;
  verifiedAt: Date;
  valid: boolean;
  provider: 'trustedform' | 'jornaya';
  responseData: any;
  errorMessage?: string;
}

export interface TCPAFormData {
  trustedform_cert?: string;
  jornaya_leadid?: string;
  tcpa_timestamp?: string;
  tcpa_ip?: string;
  consent_tcpa?: boolean;
}

export interface TCPAProviderResponse {
  valid: boolean;
  data?: any;
  error?: string;
}
