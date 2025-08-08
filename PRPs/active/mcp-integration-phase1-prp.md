# PRP: MCP Integration Phase 1 - Critical Connections

> **Connect Priority P0 MCPs to enable direct service operations for agents**

## 🎯 Goal
Connect the 5 critical MCPs (Supabase, GitHub, Playwright, BigQuery, DBT) that are required by the most agents and provide the highest value.

## 🔑 Why This Matters
- **User Value**: Agents can directly operate services instead of just generating code
- **Business Value**: Faster development with fewer errors
- **Technical Value**: Direct API access eliminates code generation mistakes

## ✅ Success Criteria
- [ ] All 5 P0 MCPs connected and operational
- [ ] Agents can authenticate and use their MCPs
- [ ] `/mcp-status` shows 100% P0 coverage
- [ ] Test operations work for each MCP
- [ ] Documentation updated with examples

## 📚 Required Context

### MCPs to Connect (Priority Order)
1. **Supabase MCP** - 12 agents need this
2. **GitHub MCP** - 8 agents need this  
3. **Playwright MCP** - Testing agents
4. **BigQuery Toolbox** - Analytics agents
5. **DBT MCP** - Data transformation

### Configuration Files
- `.claude/config/mcp-registry.json` - Registry of all MCPs
- `.claude/agents/*.md` - Agent MCP requirements
- `.claude/commands/mcp-status.md` - Status checking

## 🏗️ Implementation Tasks

### Task 1: Connect Supabase MCP
```bash
# Install Supabase MCP
npm install @supabase/mcp-server

# Configure connection
{
  "supabase-mcp": {
    "url": process.env.SUPABASE_URL,
    "key": process.env.SUPABASE_ANON_KEY,
    "service_key": process.env.SUPABASE_SERVICE_KEY
  }
}

# Test with database-architect
/test-mcp database-architect supabase-mcp
```

### Task 2: Connect GitHub MCP
```bash
# Install GitHub MCP
npm install @github/mcp-server

# Configure with token
{
  "github-mcp": {
    "token": process.env.GITHUB_TOKEN,
    "owner": "bearingfruitco",
    "repo": "debt-funnel"
  }
}

# Test with senior-engineer
/test-mcp senior-engineer github-mcp
```

### Task 3: Connect Playwright MCP
```bash
# Install Playwright MCP
npm install @microsoft/playwright-mcp

# Configure browser settings
{
  "playwright-mcp": {
    "headless": true,
    "browsers": ["chromium"],
    "timeout": 30000
  }
}

# Test with qa agent
/test-mcp qa playwright-mcp
```

### Task 4: Connect BigQuery Toolbox
```bash
# Install BigQuery MCP
npm install @google/bigquery-mcp

# Configure credentials
{
  "bigquery-mcp": {
    "project": process.env.GCP_PROJECT,
    "credentials": "./bigquery-key.json"
  }
}

# Test with analytics-engineer
/test-mcp analytics-engineer bigquery-mcp
```

### Task 5: Connect DBT MCP
```bash
# Install DBT MCP
npm install @dbt/mcp-server

# Configure project
{
  "dbt-mcp": {
    "project_dir": "./dbt",
    "profiles_dir": "./dbt",
    "target": "prod"
  }
}

# Test with database-architect
/test-mcp database-architect dbt-mcp
```

## 🧪 Validation

### Per-MCP Testing
- [ ] Authentication works
- [ ] Basic operations succeed
- [ ] Permissions are enforced
- [ ] Error handling works

### Integration Testing
- [ ] Agent can use MCP in workflow
- [ ] Multiple agents can share MCP
- [ ] Performance is acceptable
- [ ] No conflicts between MCPs

## 📊 Success Metrics
- **Coverage**: 5/5 P0 MCPs connected
- **Agents Enabled**: 15+ agents with MCP access
- **Operations**: Direct service calls working
- **Performance**: <100ms MCP response time
