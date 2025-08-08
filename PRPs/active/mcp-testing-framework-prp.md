# PRP: MCP Testing Framework

> **Create testing framework to verify MCP connections and agent access**

## 🎯 Goal
Build a testing system that verifies each MCP connection works and agents can properly access their required services.

## 🔑 Why This Matters
- **User Value**: Confidence that agents can perform operations
- **Business Value**: Prevent runtime failures
- **Technical Value**: Early detection of permission issues

## ✅ Success Criteria
- [ ] Test command `/test-mcp` created
- [ ] Automated test suite for all MCPs
- [ ] Permission validation per agent
- [ ] Performance benchmarking
- [ ] Clear error reporting

## 📚 Required Context

### Test Requirements
- Verify authentication
- Test basic operations
- Check permissions
- Measure response times
- Handle errors gracefully

## 🏗️ Implementation Tasks

### Task 1: Create Test Command
```typescript
// .claude/commands/test-mcp.md
/test-mcp                    # Test all MCPs
/test-mcp [mcp-name]        # Test specific MCP
/test-mcp [agent] [mcp]     # Test agent access
```

### Task 2: MCP Test Suite
```typescript
class MCPTester {
  async testSupabaseMCP() {
    // Test connection
    const connected = await supabase.connect();
    
    // Test read
    const data = await supabase.from('test').select();
    
    // Test write
    const insert = await supabase.from('test').insert({});
    
    // Test permissions
    const rls = await supabase.rls.getPolicies();
    
    return { success: true, operations: 4 };
  }
  
  async testGitHubMCP() {
    // Test auth
    const user = await github.getAuthenticatedUser();
    
    // Test repo access
    const repo = await github.getRepo('owner/repo');
    
    // Test issue creation
    const issue = await github.createIssue({ title: 'Test' });
    
    return { success: true, operations: 3 };
  }
}
```

### Task 3: Agent Access Testing
```typescript
async function testAgentMCPAccess(agent: string, mcp: string) {
  // Load agent permissions
  const permissions = getAgentPermissions(agent, mcp);
  
  // Test each permission
  for (const perm of permissions) {
    const result = await testPermission(mcp, perm);
    if (!result.success) {
      return { error: `Failed: ${perm}` };
    }
  }
  
  return { success: true, permissions: permissions.length };
}
```

### Task 4: Performance Testing
```typescript
async function benchmarkMCP(mcp: string) {
  const operations = ['read', 'write', 'list', 'delete'];
  const results = {};
  
  for (const op of operations) {
    const start = Date.now();
    await performOperation(mcp, op);
    results[op] = Date.now() - start;
  }
  
  return results;
}
```

### Task 5: Test Report Generation
```typescript
function generateTestReport(results) {
  const report = [];
  
  report.push('# MCP Test Results\n');
  
  // Summary
  const passed = results.filter(r => r.success).length;
  report.push(`✅ Passed: ${passed}/${results.length}\n`);
  
  // Details per MCP
  for (const result of results) {
    report.push(`## ${result.mcp}`);
    report.push(`Status: ${result.success ? '✅' : '❌'}`);
    report.push(`Operations: ${result.operations}`);
    report.push(`Response: ${result.avgTime}ms\n`);
  }
  
  return report.join('\n');
}
```

## 🧪 Validation
- [ ] All MCPs have test coverage
- [ ] Agent permission tests work
- [ ] Performance benchmarks accurate
- [ ] Error cases handled
- [ ] Reports are clear

## 📊 Success Metrics
- **Test Coverage**: 100% of MCPs
- **Agent Coverage**: 100% of agents
- **Performance**: <100ms average
- **Reliability**: 99% test pass rate
