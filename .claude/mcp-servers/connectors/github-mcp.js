/**
 * GitHub MCP Connector
 * Provides repository operations for agents
 */

require('dotenv').config();
const { Octokit } = require('@octokit/rest');

class GitHubMCP {
  constructor() {
    this.client = null;
    this.connected = false;
    this.owner = null;
    this.repo = null;
  }

  async connect() {
    try {
      const token = process.env.GITHUB_TOKEN;
      
      if (!token) {
        throw new Error('Missing GitHub token');
      }

      this.client = new Octokit({
        auth: token
      });

      // Get authenticated user to verify connection
      const { data: user } = await this.client.users.getAuthenticated();
      this.connected = true;
      
      // Set default repo from environment or detect
      this.owner = process.env.GITHUB_OWNER || 'bearingfruitco';
      this.repo = process.env.GITHUB_REPO || 'debt-funnel';
      
      console.log(`✅ GitHub MCP connected as ${user.login}`);
      return true;
    } catch (error) {
      console.error('❌ GitHub MCP connection failed:', error.message);
      return false;
    }
  }

  async testConnection() {
    if (!this.connected) {
      await this.connect();
    }

    try {
      const { data: user } = await this.client.users.getAuthenticated();
      
      return {
        success: true,
        message: `Connected as ${user.login}`,
        capabilities: [
          'repos:manage',
          'issues:crud',
          'prs:create',
          'actions:trigger',
          'gists:manage'
        ]
      };
    } catch (error) {
      return {
        success: false,
        message: error.message
      };
    }
  }

  // Repository operations
  async getRepo(owner = this.owner, repo = this.repo) {
    return await this.client.repos.get({ owner, repo });
  }

  async createBranch(branchName, baseBranch = 'main') {
    const { data: ref } = await this.client.git.getRef({
      owner: this.owner,
      repo: this.repo,
      ref: `heads/${baseBranch}`
    });

    return await this.client.git.createRef({
      owner: this.owner,
      repo: this.repo,
      ref: `refs/heads/${branchName}`,
      sha: ref.object.sha
    });
  }

  // Issue operations
  async createIssue(title, body, labels = []) {
    return await this.client.issues.create({
      owner: this.owner,
      repo: this.repo,
      title,
      body,
      labels
    });
  }

  async getIssue(issueNumber) {
    return await this.client.issues.get({
      owner: this.owner,
      repo: this.repo,
      issue_number: issueNumber
    });
  }

  async listIssues(options = {}) {
    return await this.client.issues.listForRepo({
      owner: this.owner,
      repo: this.repo,
      ...options
    });
  }

  async updateIssue(issueNumber, updates) {
    return await this.client.issues.update({
      owner: this.owner,
      repo: this.repo,
      issue_number: issueNumber,
      ...updates
    });
  }

  // Pull Request operations
  async createPR(title, head, base = 'main', body = '') {
    return await this.client.pulls.create({
      owner: this.owner,
      repo: this.repo,
      title,
      head,
      base,
      body
    });
  }

  async getPR(prNumber) {
    return await this.client.pulls.get({
      owner: this.owner,
      repo: this.repo,
      pull_number: prNumber
    });
  }

  async listPRs(options = {}) {
    return await this.client.pulls.list({
      owner: this.owner,
      repo: this.repo,
      ...options
    });
  }

  async mergePR(prNumber, options = {}) {
    return await this.client.pulls.merge({
      owner: this.owner,
      repo: this.repo,
      pull_number: prNumber,
      ...options
    });
  }

  // File operations
  async getFile(path, branch = 'main') {
    return await this.client.repos.getContent({
      owner: this.owner,
      repo: this.repo,
      path,
      ref: branch
    });
  }

  async createOrUpdateFile(path, content, message, branch = 'main') {
    // Get current file to get SHA if it exists
    let sha;
    try {
      const { data: currentFile } = await this.getFile(path, branch);
      sha = currentFile.sha;
    } catch (error) {
      // File doesn't exist, will create new
    }

    return await this.client.repos.createOrUpdateFileContents({
      owner: this.owner,
      repo: this.repo,
      path,
      message,
      content: Buffer.from(content).toString('base64'),
      branch,
      sha
    });
  }

  // Actions operations
  async triggerWorkflow(workflowId, inputs = {}) {
    return await this.client.actions.createWorkflowDispatch({
      owner: this.owner,
      repo: this.repo,
      workflow_id: workflowId,
      ref: 'main',
      inputs
    });
  }

  async getWorkflowRuns(workflowId) {
    return await this.client.actions.listWorkflowRuns({
      owner: this.owner,
      repo: this.repo,
      workflow_id: workflowId
    });
  }
}

module.exports = GitHubMCP;
