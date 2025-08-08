---
name: mcp-status
description: Check MCP connections and agent mappings
aliases: [mcp, check-mcp, mcp-connections]
---

# MCP Status Command

Shows which MCPs are connected and which agents have access to them.

## Usage

```bash
/mcp-status              # Show all MCP connections
/mcp-status [agent]      # Show MCPs for specific agent
/mcp-status --missing    # Show missing required MCPs
/mcp-status --priority   # Show by priority order
```

## Process

### Phase 1: Load Configuration

```javascript
function loadMCPConfig() {
  const registry = JSON.parse(
    fs.readFileSync('.claude/config/mcp-registry.json', 'utf8')
  );
  
  const connected = checkConnectedMCPs();
  
  return {
    registry,
    connected,
    missing: findMissingMCPs(registry, connected)
  };
}
```

### Phase 2: Check Agent Requirements

```javascript
function checkAgentMCPs(agentName) {
  const agentFile = `.claude/agents/${agentName}.md`;
  const content = fs.readFileSync(agentFile, 'utf8');
  
  // Extract MCP requirements from frontmatter
  const match = content.match(/mcp_requirements:([\s\S]*?)---/);
  if (!match) return null;
  
  const yaml = parseYAML(match[1]);
  
  return {
    agent: agentName,
    required: yaml.required || [],
    optional: yaml.optional || [],
    permissions: yaml.mcp_permissions || {}
  };
}
```

### Phase 3: Generate Status Report

```javascript
function generateMCPStatus() {
  const config = loadMCPConfig();
  const agents = getAllAgents();
  
  const report = [];
  
  // Overall status
  report.push('# 🔌 MCP Connection Status\n');
  report.push(`Connected: ${config.connected.length}/${Object.keys(config.registry.available_mcps).length}`);
  report.push(`Agents configured: ${agents.withMCP.length}/${agents.total}\n`);
  
  // Priority MCPs
  report.push('## 🎯 Priority P0 MCPs (Critical)\n');
  for (const mcp of config.registry.mcp_priority_groups.P0_critical) {
    const status = config.connected.includes(mcp) ? '✅' : '❌';
    const info = config.registry.available_mcps[mcp];
    report.push(`${status} ${info.name}`);
    report.push(`   ${info.url}`);
    
    // Show which agents need this
    const needingAgents = findAgentsNeedingMCP(mcp);
    if (needingAgents.length > 0) {
      report.push(`   Required by: ${needingAgents.join(', ')}`);
    }
    report.push('');
  }
  
  // Agent coverage
  report.push('## 🤖 Agent MCP Coverage\n');
  for (const agent of agents.all) {
    const mcps = checkAgentMCPs(agent);
    if (!mcps) continue;
    
    const coverage = calculateCoverage(mcps, config.connected);
    const emoji = coverage === 100 ? '✅' : coverage >= 50 ? '🟡' : '❌';
    
    report.push(`${emoji} ${agent} (${coverage}% coverage)`);
    report.push(`   Required: ${mcps.required.join(', ') || 'none'}`);
    report.push(`   Optional: ${mcps.optional.join(', ') || 'none'}`);
    report.push('');
  }
  
  return report.join('\n');
}
```

## Output Example

```bash
/mcp-status

# 🔌 MCP Connection Status

Connected: 5/18
Agents configured: 12/30

## 🎯 Priority P0 MCPs (Critical)

✅ Supabase MCP
   https://supabase.com/docs/guides/getting-started/mcp
   Required by: database-architect, backend, senior-engineer

✅ GitHub MCP
   https://github.com/github/github-mcp-server
   Required by: senior-engineer, security-auditor

❌ DBT MCP
   https://docs.getdbt.com/docs/dbt-cloud-apis/mcp
   Required by: database-architect, analytics-engineer

❌ BigQuery Toolbox
   https://googleapis.github.io/genai-toolbox/resources/sources/bigquery/
   Required by: analytics-engineer, event-schema

❌ Playwright MCP
   https://github.com/microsoft/playwright-mcp
   Required by: qa, playwright-specialist

## 🤖 Agent MCP Coverage

✅ database-architect (100% coverage)
   Required: supabase-mcp, dbt-mcp, bigquery-toolbox
   Optional: airbyte-mcp

🟡 senior-engineer (66% coverage)
   Required: github-mcp, supabase-mcp, sentry-mcp
   Optional: ref-tools-mcp, octocode-mcp

❌ analytics-engineer (0% coverage)
   Required: bigquery-toolbox, dbt-mcp, airbyte-mcp
   Optional: supabase-mcp

## 📊 Summary

Critical Missing MCPs:
1. DBT MCP - Needed by 3 agents
2. BigQuery Toolbox - Needed by 2 agents
3. Playwright MCP - Needed by 2 agents

Next Steps:
1. Connect DBT MCP for data transformations
2. Connect BigQuery for analytics
3. Connect Playwright for testing
```

## Visual Matrix

```bash
/mcp-status --matrix

         | Supa | GH  | DBT | BQ  | PW  | STG | SEN |
---------|------|-----|-----|-----|-----|-----|-----|
db-arch  |  ✅  |  -  | ✅  | ✅  |  -  |  -  |  -  |
senior   |  ✅  | ✅  |  -  |  -  |  -  |  -  | ✅  |
frontend |  -   |  -  |  -  |  -  | ⚪  | ✅  |  -  |
backend  |  ✅  |  -  |  -  | ⚪  |  -  |  -  |  -  |
qa       |  -   |  -  |  -  |  -  | ✅  | ✅  | ⚪  |

Legend: ✅ Required | ⚪ Optional | - Not needed
```

## Integration Check

```javascript
// Check if agent can use its MCPs
async function testAgentMCPAccess(agentName) {
  const mcps = checkAgentMCPs(agentName);
  const results = [];
  
  for (const mcp of mcps.required) {
    const canAccess = await testMCPConnection(mcp);
    results.push({
      mcp,
      status: canAccess ? 'connected' : 'missing',
      required: true
    });
  }
  
  return results;
}
```

This gives visibility into MCP connections!
