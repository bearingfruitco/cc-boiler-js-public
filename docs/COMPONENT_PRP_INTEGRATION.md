# Component PRP Workflow Integration

## Overview

The component PRP generation system is designed to work seamlessly with our existing PRP workflow. Here's how it integrates:

## Integration Points

### 1. PRP Writer Agent
When generating component PRPs, the system uses the specialized `/spawn prp-writer` agent that:
- Understands the complete PRP template structure
- Follows established validation loop patterns
- Maintains consistency with manually created PRPs
- Integrates with existing PRP tracking systems

### 2. PRP Tracking System
Generated component PRPs are automatically registered in:
- `PRPs/active_prps.json` - Central tracking file
- `PRPs/active/` directory - Where all active PRPs live
- PRP status tracking - Marked as "ready" initially

### 3. Validation Commands
Component PRPs work with all existing PRP commands:
- `/prp-execute [component-name]` - Run validation loops
- `/prp-status` - See all PRPs including generated ones
- `/prp-chain` - Include in PRP execution chains
- `/prp-validate` - Validate PRP structure

### 4. Workflow Commands
Seamless integration with feature workflow:
- `/fw start [component-name]` - Begin implementation
- `/fw track` - Monitor progress
- `/fw complete [component-name]` - Mark as done

## How Component PRPs Enhance the System

### Automatic Discovery
Instead of manually identifying what needs to be built:
1. Architecture documents are parsed
2. Components are automatically identified
3. Dependencies are mapped
4. Priority is assigned based on architecture

### Consistent Structure
Every generated PRP follows the exact same structure:
- Overview and goals
- Technical context from architecture
- 4-level validation loops
- Design system compliance
- Security requirements
- Performance benchmarks

### Architecture Traceability
Each component PRP:
- Links back to architecture documents
- References specific sections
- Maintains architectural decisions
- Ensures implementation matches design

## Workflow Comparison

### Traditional PRP Creation
```bash
/prd                    # Create product requirements
/create-prp feature-x   # Manually create PRP
/prp-execute feature-x  # Validate
/fw start feature-x     # Implement
```

### Architecture-Driven Component PRPs
```bash
/prd                       # Create product requirements
/create-architecture       # Generate architecture
/generate-component-prps   # Auto-generate all PRPs
/prp-execute auth-service  # Validate specific component
/fw start auth-service     # Implement
```

## No Breaking Changes

The component PRP system:
- ✅ Uses the same PRP format
- ✅ Works with existing commands
- ✅ Follows established patterns
- ✅ Integrates with tracking systems
- ✅ Compatible with validation loops

## Enhanced Capabilities

### 1. Bulk Generation
Generate PRPs for all components at once:
```bash
/generate-component-prps           # All components
/generate-component-prps --priority # High priority only
```

### 2. Architecture Sync
PRPs stay synchronized with architecture:
```bash
/validate-architecture    # Check architecture
/generate-component-prps  # Regenerate PRPs if needed
```

### 3. Dependency Management
Components are generated in dependency order:
- Authentication before protected features
- Database layer before API layer
- Shared components before consumers

## Using the PRP Writer Agent

When you need to create PRPs manually with the same quality:

```bash
# Spawn the PRP writer for custom PRPs
/spawn prp-writer "Create PRP for custom notification system"

# The agent will:
# 1. Ask for component details
# 2. Review architecture if needed
# 3. Generate comprehensive PRP
# 4. Ensure all sections are complete
```

## Best Practices

### 1. Architecture First
Always create architecture before generating component PRPs:
```bash
/chain create-architecture && /validate-architecture && /generate-component-prps
```

### 2. Review Generated PRPs
While generated PRPs are comprehensive, always review them:
- Check component scope is correct
- Verify dependencies are accurate
- Adjust priorities if needed
- Add project-specific details

### 3. Use with Existing PRPs
Component PRPs complement manual PRPs:
- Components from architecture → Generated PRPs
- Unique features → Manual PRPs with `/create-prp`
- Both work together seamlessly

### 4. Maintain Architecture
As system evolves:
1. Update architecture documents
2. Re-run `/generate-component-prps`
3. New components get PRPs automatically
4. Existing PRPs are preserved

## Command Integration Map

```
/create-architecture
    ↓
/validate-architecture
    ↓
/generate-component-prps ←── /spawn prp-writer
    ↓
/prp-execute [component] ←── Same as manual PRPs
    ↓
/fw start [component] ←── Same workflow system
    ↓
/prp-complete [component] ←── Same completion
```

## Summary

The component PRP generation enhances our existing PRP system without breaking anything. It adds:
- Automatic component discovery from architecture
- Bulk PRP generation with consistency
- Architecture-driven development workflow
- Full integration with existing commands

All while maintaining compatibility with the manual PRP creation process and existing validation systems!
