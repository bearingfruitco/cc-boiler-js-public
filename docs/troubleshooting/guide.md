# Troubleshooting Guide

> Common issues and solutions for Claude Code Boilerplate v4.0.0

## 🚨 Quick Fixes

### Command Not Found
```bash
# Problem: /sr: command not found
# Solution:
cd /path/to/project
/sr  # Must be in project root with .claude folder
```

### Context Too Large
```bash
# Problem: Token limit exceeded
# Solution:
/compress               # Intelligent context compression
/cp save minimal       # Save minimal context
/dc clear              # Clear doc cache
```

### Design Validation Errors
```bash
# Problem: Design system violations blocking saves
# Solution:
/dmoff                 # Temporarily disable (not recommended)
/vd --fix             # Auto-fix violations
# Or fix manually following rules:
# - Font sizes: text-size-[1-4]
# - Font weights: font-regular, font-semibold
# - Spacing: p-1, p-2, p-3, p-4, p-6, p-8
```

## 📋 Common Issues

### 1. Git Pre-Commit Hook Failures

**Problem**: Commit blocked by validation errors
```
husky - pre-commit hook exited with code 1
```

**Solutions**:
```bash
# Check what failed
npm run typecheck
npm run lint
npm test

# Fix design issues
npm run check:design:staged

# Skip hooks (emergency only)
git commit --no-verify -m "emergency fix"
```

### 2. Agent Orchestration Issues

**Problem**: Agents not coordinating properly
```
Error: Multiple agents trying to edit same file
```

**Solutions**:
```bash
# Reset agent states
/sas --reset

# Use sequential orchestration
/spawn frontend
# Wait for completion
/spawn backend

# Check agent boundaries
/agent-health
```

### 3. PRP Validation Failures

**Problem**: PRP execution failing at various levels
```
❌ Level 2 validation failed: No tests found
```

**Solutions**:
```bash
# Run specific level with verbose output
/prp-execute feature --level 2 --verbose

# Auto-fix common issues
/prp-execute feature --fix

# Skip to specific level
/prp-execute feature --skip-to 3
```

### 4. Context Loss Between Sessions

**Problem**: Lost work after Claude Code restart
```
Error: No checkpoint found
```

**Solutions**:
```bash
# Always use smart resume
/sr

# Create manual checkpoints
/checkpoint create before-risky-change

# Check GitHub gist saves
/sas --check-gist

# Restore from backup
/checkpoint list
/checkpoint restore [name]
```

### 5. Integration Conflicts

**Problem**: Existing project integration issues
```
Error: Command conflicts detected
```

**Solutions**:
```bash
# Use project-specific commands
/cc-project         # Your original command
/cc                 # Boilerplate command

# Check integration report
cat .claude-integration/INTEGRATION_COMPLETE.md

# Rollback if needed
/integration-rollback
```

### 6. Performance Issues

**Problem**: Slow command execution
```
Command taking longer than expected...
```

**Solutions**:
```bash
# Check system performance
/performance-monitor check

# Disable non-critical hooks
/perf-mode on

# Clear caches
/cache clear
/dc clear

# Reduce parallel operations
/config set orchestration.max_parallel 2
```

### 7. Dependency Tracking Errors

**Problem**: False dependency warnings
```
Warning: Component has 5 dependents but only 3 found
```

**Solutions**:
```bash
# Rescan all dependencies
/deps scan --force

# Check specific component
/deps check Button --verbose

# Fix dependency comments
/deps fix
```

### 8. Visual Debugging Not Working

**Problem**: Ctrl+V not analyzing screenshots
```
No image data found in clipboard
```

**Solutions**:
1. Ensure screenshot is in clipboard (not file)
2. Try alternative method:
   ```bash
   /vp debug-ui
   # Then paste when prompted
   ```
3. Check Claude Code version supports visual features

### 9. Chain Automation Failures

**Problem**: Chains not triggering or failing mid-execution
```
Chain 'morning-setup' failed at step 3
```

**Solutions**:
```bash
# Check chain status
/chain status

# Run specific step
/chain run morning-setup --from-step 3

# Debug chain conditions
/chain debug morning-setup

# Disable auto-triggers
/chain config auto-trigger false
```

### 10. Async Event System Issues

**Problem**: Events not firing or blocking UI
```
Warning: Synchronous event detected
```

**Solutions**:
```bash
# Validate async patterns
/validate-async

# Check event queue
/events status

# Clear stuck events
/events clear

# Use fire-and-forget pattern
/create-event-handler user-action
```

## 🔧 Advanced Troubleshooting

### Debug Mode
```bash
# Enable debug logging
/debug on

# Check hook execution
/debug hooks

# Trace command execution
/debug trace /cc Button

# Export debug logs
/debug export
```

### System Health Check
```bash
# Full system diagnostic
/health

# Specific subsystem checks
/health hooks
/health agents  
/health context
/health performance
```

### Recovery Procedures

#### Complete Reset
```bash
# Backup current state
/checkpoint create pre-reset

# Reset to clean state
/reset --keep-data

# Restore from backup if needed
/checkpoint restore pre-reset
```

#### Partial Recovery
```bash
# Fix corrupt context
/context repair

# Rebuild command index
/commands rebuild

# Reset agent states
/agents reset

# Clear all caches
/cache clear --all
```

## 📊 Error Codes Reference

| Code | Meaning | Solution |
|------|---------|----------|
| CLB-001 | Context overflow | Use /compress |
| CLB-002 | Design violation | Fix design tokens |
| CLB-003 | Security block | Check PII handling |
| CLB-004 | Agent conflict | Reset agent states |
| CLB-005 | Hook failure | Check hook logs |
| CLB-006 | Integration issue | Review integration |
| CLB-007 | Validation failure | Run level checks |
| CLB-008 | Performance limit | Optimize code |

## 🆘 Getting Help

### Self-Help Resources
1. Run `/help` for context-aware assistance
2. Check `/docs` for documentation
3. Use `/examples` for patterns
4. Review `/logs` for details

### Community Support
- GitHub Issues: Report bugs
- Discussions: Ask questions
- Wiki: Community solutions

### Emergency Contacts
- Critical bugs: [create issue with 'critical' label]
- Security issues: [security@example.com]

## 💡 Prevention Tips

### Daily Practices
1. Always start with `/sr`
2. Create checkpoints before major changes
3. Run validation early and often
4. Use the right agent for the task
5. Follow design system strictly

### Weekly Maintenance
1. Clear old checkpoints
2. Update dependencies
3. Review error logs
4. Optimize context usage
5. Extract successful patterns

### Project Setup
1. Configure Git hooks properly
2. Set up environment variables
3. Initialize field registry
4. Configure agent boundaries
5. Test integration thoroughly

## 📚 Related Documentation

- [Development Guide](./README.md)
- [System Overview](../SYSTEM_OVERVIEW.md)
- [Integration Guide](../setup/EXISTING_PROJECT_INTEGRATION.md)
- [Workflow Guide](../workflow/README.md)
