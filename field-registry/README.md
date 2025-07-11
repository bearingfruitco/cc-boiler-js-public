# Field Registry System

This registry defines all data fields used across our forms and applications, with built-in security classifications and compliance requirements.

## Structure

- **core/** - Universal tracking fields needed in most projects
- **verticals/** - Industry-specific fields (debt, healthcare, etc.)
- **compliance/** - Security and regulatory classifications
- **generators/** - Tools to generate type-safe code from registry

## Security Classifications

Each field has security metadata:

```json
{
  "fieldName": {
    "type": "STRING",
    "pii": true,              // Personal Identifiable Information
    "phi": false,             // Protected Health Information
    "sensitive": true,        // Requires encryption
    "prepopulate": false,     // Can be populated from URL params
    "clientVisible": false,   // Can be exposed to client-side
    "auditLog": true,        // Requires audit trail
    "encryption": "field",    // none | transit | field
    "masking": "partial"      // none | partial | full
  }
}
```

## Usage

### 1. Generate a Secure Form

```bash
/create-tracked-form contact --vertical=debt
```

This will:
- Load core tracking fields
- Add debt-specific fields
- Generate form with security rules
- Create validation schemas
- Add compliance checks

### 2. Validate Field Security

```bash
/audit-form-security components/forms/LeadForm.tsx
```

### 3. Generate TypeScript Types

```bash
/generate-field-types
```

## Security Rules

### PII Protection
- PII fields NEVER logged to console
- PII fields NEVER in localStorage
- PII fields NEVER in URL parameters
- PII fields encrypted at rest
- PII fields require audit logging

### Prepopulation Rules
Only these fields can be prepopulated from URL:
- UTM parameters (utm_source, utm_medium, etc.)
- Campaign/Partner IDs
- Non-PII tracking parameters

### Data Flow
```
URL Params → Sanitization → Whitelist Check → Form
     ↓                                           ↓
   Block PII                              Server-Side Only
```

## Compliance

### Standard Mode
- Basic PII protection
- Standard encryption
- 90-day retention

### HIPAA Mode
- PHI field encryption
- Detailed audit logs
- Access controls
- 7-year retention

### GDPR Mode
- Consent tracking
- Right to deletion
- Data portability
- 30-day deletion
