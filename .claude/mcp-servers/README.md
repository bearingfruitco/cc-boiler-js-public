# MCP Connection Implementation

This directory contains the actual MCP server connections and configurations.

## Structure

```
.claude/mcp-servers/
├── README.md                   # This file
├── package.json                # MCP dependencies
├── config.json                 # MCP connection configs
├── connectors/
│   ├── supabase-mcp.js       # Supabase MCP connector
│   ├── github-mcp.js          # GitHub MCP connector
│   ├── playwright-mcp.js      # Playwright MCP connector
│   ├── bigquery-mcp.js        # BigQuery MCP connector
│   └── dbt-mcp.js             # DBT MCP connector
└── test/
    └── test-connections.js     # Test all MCP connections
```

## Priority P0 MCPs

1. **Supabase MCP** - Database operations (12 agents need this)
2. **GitHub MCP** - Repository management (8 agents need this)
3. **Playwright MCP** - Test automation (QA agents)
4. **BigQuery Toolbox** - Analytics (analytics agents)
5. **DBT MCP** - Data transformations (data agents)

## Installation

```bash
cd .claude/mcp-servers
npm install
```

## Configuration

Set environment variables in `.env`:

```env
# Supabase
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# GitHub
GITHUB_TOKEN=your-github-token

# BigQuery
GCP_PROJECT=your-gcp-project
GOOGLE_APPLICATION_CREDENTIALS=./bigquery-key.json

# DBT
DBT_PROJECT_DIR=./dbt
DBT_PROFILES_DIR=./dbt
```

## Testing

```bash
npm test
# or
/test-mcp supabase-mcp
```

## Status

- [ ] Supabase MCP
- [ ] GitHub MCP
- [ ] Playwright MCP
- [ ] BigQuery Toolbox
- [ ] DBT MCP
