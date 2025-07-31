---
name: validate-pii-handling
description: Validate PII handling in code
category: security
---

# Validate PII Handling

This command validates that personally identifiable information (PII) is properly handled in the codebase.

## Usage
```
/validate-pii-handling [file|directory]
```

## What it checks:
- Proper masking of sensitive fields
- Secure storage practices
- Audit logging for PII access
- Compliance with data protection policies

Note: This functionality is also covered by the PII protection hook (07-pii-protection.py).
