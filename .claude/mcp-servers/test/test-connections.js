/**
 * Test MCP Connections
 * Verifies all MCP servers are properly connected
 */

const chalk = require('chalk');
const SupabaseMCP = require('../connectors/supabase-mcp');
const GitHubMCP = require('../connectors/github-mcp');

// Test results storage
const results = {
  passed: [],
  failed: [],
  skipped: []
};

// Available MCP testers
const mcpTesters = {
  supabase: testSupabase,
  github: testGitHub,
  playwright: testPlaywright,
  bigquery: testBigQuery,
  dbt: testDBT
};

async function testSupabase() {
  console.log(chalk.blue('\n📊 Testing Supabase MCP...'));
  
  const supabase = new SupabaseMCP();
  const result = await supabase.testConnection();
  
  if (result.success) {
    console.log(chalk.green('✅ Supabase MCP: PASSED'));
    console.log(chalk.gray(`   Capabilities: ${result.capabilities.join(', ')}`));
    results.passed.push('supabase-mcp');
  } else {
    console.log(chalk.red('❌ Supabase MCP: FAILED'));
    console.log(chalk.red(`   Error: ${result.message}`));
    results.failed.push('supabase-mcp');
  }
  
  return result;
}

async function testGitHub() {
  console.log(chalk.blue('\n🐙 Testing GitHub MCP...'));
  
  const github = new GitHubMCP();
  const result = await github.testConnection();
  
  if (result.success) {
    console.log(chalk.green('✅ GitHub MCP: PASSED'));
    console.log(chalk.gray(`   ${result.message}`));
    console.log(chalk.gray(`   Capabilities: ${result.capabilities.join(', ')}`));
    results.passed.push('github-mcp');
  } else {
    console.log(chalk.red('❌ GitHub MCP: FAILED'));
    console.log(chalk.red(`   Error: ${result.message}`));
    results.failed.push('github-mcp');
  }
  
  return result;
}

async function testPlaywright() {
  console.log(chalk.blue('\n🎭 Testing Playwright MCP...'));
  console.log(chalk.yellow('⚠️  Playwright MCP: Not yet implemented'));
  results.skipped.push('playwright-mcp');
  return { success: false, message: 'Not implemented' };
}

async function testBigQuery() {
  console.log(chalk.blue('\n📈 Testing BigQuery MCP...'));
  console.log(chalk.yellow('⚠️  BigQuery MCP: Not yet implemented'));
  results.skipped.push('bigquery-mcp');
  return { success: false, message: 'Not implemented' };
}

async function testDBT() {
  console.log(chalk.blue('\n🔄 Testing DBT MCP...'));
  console.log(chalk.yellow('⚠️  DBT MCP: Not yet implemented'));
  results.skipped.push('dbt-mcp');
  return { success: false, message: 'Not implemented' };
}

async function runTests() {
  console.log(chalk.bold.blue('================================='));
  console.log(chalk.bold.blue('    MCP Connection Test Suite    '));
  console.log(chalk.bold.blue('================================='));
  
  const specificMCP = process.argv[2];
  
  if (specificMCP) {
    // Test specific MCP
    if (mcpTesters[specificMCP]) {
      await mcpTesters[specificMCP]();
    } else {
      console.log(chalk.red(`Unknown MCP: ${specificMCP}`));
      console.log(chalk.gray(`Available: ${Object.keys(mcpTesters).join(', ')}`));
    }
  } else {
    // Test all MCPs
    for (const [name, tester] of Object.entries(mcpTesters)) {
      await tester();
    }
  }
  
  // Print summary
  console.log(chalk.bold.blue('\n================================='));
  console.log(chalk.bold.blue('           Summary               '));
  console.log(chalk.bold.blue('================================='));
  
  console.log(chalk.green(`✅ Passed: ${results.passed.length}`));
  if (results.passed.length > 0) {
    results.passed.forEach(mcp => {
      console.log(chalk.gray(`   - ${mcp}`));
    });
  }
  
  console.log(chalk.red(`❌ Failed: ${results.failed.length}`));
  if (results.failed.length > 0) {
    results.failed.forEach(mcp => {
      console.log(chalk.gray(`   - ${mcp}`));
    });
  }
  
  console.log(chalk.yellow(`⚠️  Skipped: ${results.skipped.length}`));
  if (results.skipped.length > 0) {
    results.skipped.forEach(mcp => {
      console.log(chalk.gray(`   - ${mcp}`));
    });
  }
  
  const total = results.passed.length + results.failed.length + results.skipped.length;
  const percentage = Math.round((results.passed.length / total) * 100);
  
  console.log(chalk.bold(`\n📊 Success Rate: ${percentage}%`));
  
  // Exit with appropriate code
  process.exit(results.failed.length > 0 ? 1 : 0);
}

// Run tests
runTests().catch(error => {
  console.error(chalk.red('Fatal error:'), error);
  process.exit(1);
});
