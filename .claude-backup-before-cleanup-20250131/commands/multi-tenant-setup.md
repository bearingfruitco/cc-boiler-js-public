---
name: multi-tenant-setup
description: |
  Complete workflow for setting up multi-tenant SaaS architecture.
  Implements tenant isolation, RLS policies, and compliant data separation.
allowed-tools: Read, Write, SearchFiles
aliases: ["mts", "multi-tenant", "saas-setup"]
---

# 🏢 Multi-Tenant SaaS Setup Workflow

Setting up complete multi-tenant architecture for your SaaS application.

## Workflow Steps

### 1. Requirements Analysis
**Agent**: pm-orchestrator
**Task**: Define tenant isolation requirements

Key considerations:
- Data isolation level (row-level vs schema-level)
- Performance requirements
- Compliance needs (SOC2, HIPAA, etc.)
- Scaling expectations

### 2. Database Architecture
**Agent**: supabase-specialist
**Task**: Design RLS policies for tenant isolation

Implementation:
- Row-Level Security policies
- Tenant context functions
- Secure tenant switching
- Performance optimizations

### 3. Schema Design
**Agent**: orm-specialist
**Task**: Create multi-tenant schema with tenant_id

Schema patterns:
- Shared tables with tenant_id
- Tenant metadata table
- Efficient indexing strategies
- Migration patterns

### 4. Event Tracking
**Agent**: event-schema
**Task**: Design tenant-aware event tracking

Considerations:
- Tenant attribution
- Cross-tenant analytics
- Privacy boundaries
- Aggregation strategies

### 5. Backend Implementation
**Agent**: backend
**Task**: Implement tenant context middleware

Features:
- Tenant resolution from JWT/subdomain
- Request context injection
- API isolation
- Rate limiting per tenant

### 6. Privacy & Compliance
**Agent**: privacy-compliance
**Task**: Ensure tenant data privacy compliance

Requirements:
- Data isolation verification
- GDPR/CCPA per tenant
- Audit logging
- Data retention policies

### 7. UI Components
**Agent**: ui-systems
**Task**: Build tenant switcher UI components

Components:
- Tenant switcher dropdown
- Onboarding flows
- Admin panels
- Tenant settings

### 8. Deployment Configuration
**Agent**: platform-deployment
**Task**: Configure per-tenant edge routing

Setup:
- Subdomain routing
- Edge middleware
- CDN configuration
- Performance optimization

### 9. Testing
**Agent**: qa
**Task**: Test tenant isolation thoroughly

Test scenarios:
- Cross-tenant data leakage
- Performance under load
- Tenant switching
- Edge cases

### 10. Documentation
**Agent**: documentation-writer
**Task**: Document multi-tenant architecture

Documentation:
- Architecture decisions
- Setup guide
- Troubleshooting
- Best practices

## Example Implementation

### Supabase RLS Policy
```sql
-- Enable RLS
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY "tenant_isolation" ON your_table
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

### Middleware Example
```typescript
export async function tenantMiddleware(req: Request) {
  const tenantId = extractTenantId(req);
  
  // Set tenant context for RLS
  await supabase.rpc('set_current_tenant', { tenant_id: tenantId });
  
  // Add to request context
  req.tenantId = tenantId;
}
```

## Quick Start

To execute this workflow:
```bash
claude -p "/orchestrate multi-tenant SaaS setup with full isolation"
```

Or use individual steps:
```bash
claude -p "Use supabase-specialist to design RLS for multi-tenant"
claude -p "Use orm-specialist to create tenant-aware schema"
```

## Best Practices

1. **Start with RLS**: Design security first
2. **Test isolation early**: Verify no data leakage
3. **Monitor performance**: Watch for tenant-specific bottlenecks
4. **Document everything**: Future developers will thank you
5. **Plan for scale**: Design for 1000x growth

This workflow ensures secure, scalable multi-tenant architecture!
