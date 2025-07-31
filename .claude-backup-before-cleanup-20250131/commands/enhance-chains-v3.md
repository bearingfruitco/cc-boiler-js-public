---
name: enhance-chains-v3
description: Update existing workflow chains to leverage v3.0 technology agents
allowed-tools: Read, Write, SearchFiles
---

# Enhancing Workflow Chains for v3.0

I'll carefully update the existing chains to incorporate the new v3.0 technology agents where they add value.

## Step 1: Backup Current Chains

!`cp .claude/chains.json .claude/backups/chains.v3-backup-$(date +%Y%m%d-%H%M%S).json`

## Step 2: Load and Analyze Current Chains

Let me examine the current chains structure and identify enhancement opportunities...

## Step 3: Apply Enhancements

I'll enhance these specific chains:

### 1. feature-complete
Add task analysis and orchestration for complex features:
- Insert `analyze-task` after checkpoint
- Add conditional `orchestrate` for complex tasks
- Add `agent-health technology` for v3.0 validation
- Add `show-metrics` for performance tracking

### 2. daily-startup  
Add v3.0 health monitoring:
- Insert `agent-health all` after smart-resume
- Add `show-metrics dashboard` for daily metrics

### 3. performance-optimization-chain
Enhance with v3.0 specialists:
- Add `supabase-specialist` for database optimization
- Add `orm-specialist` for query optimization
- Add `ui-systems` for frontend optimization
- Add `platform-deployment` for edge optimization

### 4. feature-development-chain
Integrate v3.0 agents in planning phase:
- Add `event-schema` for data modeling
- Add `orm-specialist` for schema design
- Update implementation with v3.0 agents

## Step 4: Add New v3.0 Chains

### New Specialized Chains:
1. **database-optimization** - Focused database performance
2. **full-stack-feature** - Complete feature with all v3.0 agents
3. **privacy-implementation** - GDPR/CCPA compliance workflow
4. **tech-stack-audit** - Comprehensive v3.0 system audit

## Implementation

The enhancements maintain backward compatibility while adding v3.0 capabilities where they provide the most value. Each enhanced chain can still function without v3.0 agents if needed.

## Summary

- Enhanced 10+ existing chains with v3.0 agents
- Added 4 new specialized chains
- Maintained all existing functionality
- Improved task routing and orchestration
