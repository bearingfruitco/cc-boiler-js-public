Switch between development environments and validate configuration:

1. Display current environment
2. List available environments  
3. Validate environment files exist
4. Check required variables are set
5. Update NODE_ENV if needed
6. Display active configuration

**Usage:**
- `/env-switch` - Show current environment
- `/env-switch staging` - Switch to staging
- `/env-switch production` - Switch to production (with confirmation)

!echo "Current environment: $NODE_ENV"
!ls -la .env* | grep -E "\.env\.(development|staging|production)$"

To switch environments, set NODE_ENV and reload:
```bash
export NODE_ENV=staging
source .env.staging
```

**Safety Note:** Switching to production requires explicit confirmation.
