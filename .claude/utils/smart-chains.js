#!/usr/bin/env node

/**
 * Smart Chain System for Claude Code
 * 
 * This module implements enhanced chain functionality with:
 * - Auto-trigger conditions
 * - Prerequisites checking
 * - Success/failure handlers
 * - Context passing between steps
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class SmartChainSystem {
  constructor() {
    this.chainsPath = path.join(__dirname, '../chains.json');
    this.statePath = path.join(__dirname, '../state/chain-state.json');
    this.contextPath = path.join(__dirname, '../state/chain-context.json');
    this.loadChains();
    this.loadState();
  }

  loadChains() {
    try {
      const chainsContent = fs.readFileSync(this.chainsPath, 'utf8');
      this.chains = JSON.parse(chainsContent);
    } catch (error) {
      console.error('Error loading chains:', error);
      this.chains = { chains: {} };
    }
  }

  saveChains() {
    fs.writeFileSync(this.chainsPath, JSON.stringify(this.chains, null, 2));
  }

  loadState() {
    try {
      if (fs.existsSync(this.statePath)) {
        this.state = JSON.parse(fs.readFileSync(this.statePath, 'utf8'));
      } else {
        this.state = { running: {}, completed: {}, failed: {} };
      }
    } catch {
      this.state = { running: {}, completed: {}, failed: {} };
    }
  }

  saveState() {
    fs.writeFileSync(this.statePath, JSON.stringify(this.state, null, 2));
  }

  /**
   * Evaluate condition expressions
   * @param {Object} condition - Condition object with all/any/none arrays
   * @returns {boolean} Whether condition is met
   */
  evaluateCondition(condition) {
    if (!condition) return true;

    // Check "all" conditions (AND)
    if (condition.all) {
      for (const expr of condition.all) {
        if (!this.evaluateExpression(expr)) return false;
      }
    }

    // Check "any" conditions (OR)
    if (condition.any) {
      let anyMet = false;
      for (const expr of condition.any) {
        if (this.evaluateExpression(expr)) {
          anyMet = true;
          break;
        }
      }
      if (condition.any.length > 0 && !anyMet) return false;
    }

    // Check "none" conditions (NOT)
    if (condition.none) {
      for (const expr of condition.none) {
        if (this.evaluateExpression(expr)) return false;
      }
    }

    return true;
  }

  /**
   * Evaluate a single expression
   * @param {string} expr - Expression to evaluate
   * @returns {boolean} Result
   */
  evaluateExpression(expr) {
    // File existence: exists(path)
    if (expr.startsWith('exists(') && expr.endsWith(')')) {
      const filePath = expr.slice(7, -1);
      return fs.existsSync(filePath);
    }

    // Not exists: !exists(path)
    if (expr.startsWith('!exists(') && expr.endsWith(')')) {
      const filePath = expr.slice(8, -1);
      return !fs.existsSync(filePath);
    }

    // File count: fileCount(pattern) > n
    if (expr.includes('fileCount(')) {
      const match = expr.match(/fileCount\((.*?)\)\s*([><=]+)\s*(\d+)/);
      if (match) {
        const [, pattern, operator, count] = match;
        const files = this.countFiles(pattern);
        return this.compareValues(files, operator, parseInt(count));
      }
    }

    // Time-based: hoursSinceLastCommand > n
    if (expr.includes('hoursSinceLastCommand')) {
      const match = expr.match(/hoursSinceLastCommand\s*([><=]+)\s*(\d+)/);
      if (match) {
        const [, operator, hours] = match;
        const lastCommand = this.getLastCommandTime();
        const hoursSince = (Date.now() - lastCommand) / (1000 * 60 * 60);
        return this.compareValues(hoursSince, operator, parseInt(hours));
      }
    }

    // Days since last command
    if (expr.includes('daysSinceLastCommand')) {
      const match = expr.match(/daysSinceLastCommand\s*([><=]+)\s*(\d+)/);
      if (match) {
        const [, operator, days] = match;
        const lastCommand = this.getLastCommandTime();
        const daysSince = (Date.now() - lastCommand) / (1000 * 60 * 60 * 24);
        return this.compareValues(daysSince, operator, parseInt(days));
      }
    }

    // Is first command today
    if (expr === 'isFirstCommandToday === true') {
      return this.isFirstCommandToday();
    }

    // Execute command: exec:command
    if (expr.startsWith('exec:')) {
      const command = expr.slice(5);
      try {
        const result = execSync(command, { stdio: 'pipe' }).toString().trim();
        // If command returns a number, evaluate it
        if (!isNaN(result)) {
          return parseInt(result) === 0;
        }
        return true;
      } catch {
        return false;
      }
    }

    // File content: file:path
    if (expr.startsWith('file:')) {
      const filePath = expr.slice(5);
      return fs.existsSync(filePath);
    }

    // Git status
    if (expr === 'git.clean') {
      try {
        const status = execSync('git status --porcelain', { stdio: 'pipe' }).toString();
        return status.trim() === '';
      } catch {
        return false;
      }
    }

    // Test status
    if (expr === 'tests.passing') {
      try {
        execSync('npm test', { stdio: 'pipe' });
        return true;
      } catch {
        return false;
      }
    }

    // Default to false for unknown expressions
    return false;
  }

  /**
   * Compare two values with an operator
   */
  compareValues(a, b, operator) {
    switch (operator) {
      case '>': return a > b;
      case '<': return a < b;
      case '>=': return a >= b;
      case '<=': return a <= b;
      case '==': return a == b;
      case '===': return a === b;
      case '!=': return a != b;
      case '!==': return a !== b;
      default: return false;
    }
  }

  /**
   * Count files matching a pattern
   */
  countFiles(pattern) {
    // Simple implementation - in production would use glob
    try {
      const files = execSync(`find . -name "${pattern}" -type f | wc -l`, { stdio: 'pipe' })
        .toString()
        .trim();
      return parseInt(files);
    } catch {
      return 0;
    }
  }

  /**
   * Get timestamp of last command
   */
  getLastCommandTime() {
    try {
      const stateFile = path.join(__dirname, '../state/last-command.json');
      if (fs.existsSync(stateFile)) {
        const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
        return new Date(state.timestamp).getTime();
      }
    } catch {}
    return Date.now(); // Default to now if no history
  }

  /**
   * Check if this is the first command today
   */
  isFirstCommandToday() {
    const lastCommand = this.getLastCommandTime();
    const lastDate = new Date(lastCommand).toDateString();
    const today = new Date().toDateString();
    return lastDate !== today;
  }

  /**
   * Check if a chain should be triggered
   */
  shouldTrigger(chainName) {
    const chain = this.chains.chains[chainName];
    if (!chain || !chain.triggers) return false;

    // Evaluate trigger conditions
    if (chain.triggers.conditions) {
      return this.evaluateCondition(chain.triggers.conditions);
    }

    return false;
  }

  /**
   * Check prerequisites for a chain
   */
  checkPrerequisites(chainName) {
    const chain = this.chains.chains[chainName];
    if (!chain || !chain.prerequisites) return { passed: true };

    const result = this.evaluateCondition(chain.prerequisites);
    if (!result) {
      return {
        passed: false,
        error: chain.prerequisites.error || 'Prerequisites not met'
      };
    }

    return { passed: true };
  }

  /**
   * Execute a chain with all enhancements
   */
  async executeChain(chainName, options = {}) {
    const chain = this.chains.chains[chainName];
    if (!chain) {
      throw new Error(`Chain '${chainName}' not found`);
    }

    // Check prerequisites
    const prereqCheck = this.checkPrerequisites(chainName);
    if (!prereqCheck.passed) {
      console.error(`Prerequisites failed: ${prereqCheck.error}`);
      return { success: false, error: prereqCheck.error };
    }

    // Initialize context
    const context = {
      chainName,
      startTime: Date.now(),
      ...chain.context,
      ...options.context
    };

    // Mark chain as running
    this.state.running[chainName] = {
      startTime: context.startTime,
      currentStep: 0
    };
    this.saveState();

    try {
      // Execute steps
      const results = await this.executeSteps(chain, context);

      // Mark as completed
      delete this.state.running[chainName];
      this.state.completed[chainName] = {
        completedAt: Date.now(),
        duration: Date.now() - context.startTime,
        results
      };
      this.saveState();

      // Execute on-success handler
      if (chain['on-success']) {
        await this.executeCommand(chain['on-success'], context);
      }

      return { success: true, results };

    } catch (error) {
      // Mark as failed
      delete this.state.running[chainName];
      this.state.failed[chainName] = {
        failedAt: Date.now(),
        error: error.message
      };
      this.saveState();

      // Execute on-failure handler
      if (chain['on-failure']) {
        await this.executeCommand(chain['on-failure'], context);
      }

      return { success: false, error: error.message };
    }
  }

  /**
   * Execute chain steps
   */
  async executeSteps(chain, context) {
    const results = [];

    // Handle different step formats
    if (chain.steps) {
      for (let i = 0; i < chain.steps.length; i++) {
        const step = chain.steps[i];
        
        // Update current step
        if (this.state.running[context.chainName]) {
          this.state.running[context.chainName].currentStep = i;
          this.saveState();
        }

        // Execute based on step type
        if (typeof step === 'string') {
          // Simple command string
          const result = await this.executeCommand(step, context);
          results.push(result);
        } else if (step.command) {
          // Command with options
          const result = await this.executeCommand(step.command, context, step);
          results.push(result);
        } else if (step.agent) {
          // Agent task
          const result = await this.executeAgentTask(step, context);
          results.push(result);
        } else if (step.commands) {
          // Nested commands
          for (const cmd of step.commands) {
            const result = await this.executeCommand(cmd, context);
            results.push(result);
          }
        }

        // Handle conditional steps
        if (step.condition && !this.evaluateExpression(step.condition)) {
          console.log(`Skipping step ${i + 1} - condition not met`);
          continue;
        }

        // Save context if requested
        if (chain.context && chain.context.save) {
          this.saveContext(context, chain.context.save);
        }

        // Create checkpoint if specified
        if (chain.checkpoints && chain.checkpoints.includes(`after:${step.name || i}`)) {
          await this.createCheckpoint(context, `${context.chainName}-step-${i}`);
        }
      }
    } else if (chain.commands) {
      // Legacy format with just commands array
      for (const cmd of chain.commands) {
        const result = await this.executeCommand(cmd, context);
        results.push(result);
      }
    }

    return results;
  }

  /**
   * Execute a single command
   */
  async executeCommand(command, context, options = {}) {
    console.log(`Executing: ${command}`);
    
    // Replace variables in command
    let processedCommand = command;
    if (context) {
      processedCommand = command.replace(/\${(\w+)}/g, (match, key) => {
        return context[key] || match;
      });
    }

    // Simulate command execution
    // In real implementation, this would call Claude Code
    return {
      command: processedCommand,
      success: true,
      timestamp: Date.now()
    };
  }

  /**
   * Execute an agent task
   */
  async executeAgentTask(step, context) {
    console.log(`Agent ${step.agent}: ${step.task}`);
    
    // In real implementation, this would invoke the agent
    return {
      agent: step.agent,
      task: step.task,
      success: true,
      timestamp: Date.now()
    };
  }

  /**
   * Save context for later use
   */
  saveContext(context, keys) {
    const savedContext = {};
    for (const key of keys) {
      if (context[key] !== undefined) {
        savedContext[key] = context[key];
      }
    }
    
    fs.writeFileSync(this.contextPath, JSON.stringify(savedContext, null, 2));
  }

  /**
   * Create a checkpoint
   */
  async createCheckpoint(context, name) {
    console.log(`Creating checkpoint: ${name}`);
    // In real implementation, would call /checkpoint create
  }

  /**
   * Check all chains for triggers
   */
  checkTriggers() {
    const triggered = [];
    
    for (const [chainName, chain] of Object.entries(this.chains.chains)) {
      if (this.shouldTrigger(chainName)) {
        triggered.push({
          name: chainName,
          chain: chain,
          prompt: chain.triggers?.prompt || `Run ${chainName}?`
        });
      }
    }
    
    return triggered;
  }

  /**
   * Add or update a chain
   */
  addChain(name, chainConfig) {
    this.chains.chains[name] = chainConfig;
    this.saveChains();
  }

  /**
   * Get chain status
   */
  getStatus() {
    return {
      running: Object.keys(this.state.running).length,
      completed: Object.keys(this.state.completed).length,
      failed: Object.keys(this.state.failed).length,
      chains: this.state
    };
  }
}

// Export for use in commands
module.exports = SmartChainSystem;

// If run directly, check for triggers
if (require.main === module) {
  const system = new SmartChainSystem();
  const triggered = system.checkTriggers();
  
  if (triggered.length > 0) {
    console.log('\n🔗 Smart Chain Triggers Detected:\n');
    for (const trigger of triggered) {
      console.log(`- ${trigger.name}: ${trigger.chain.description}`);
      console.log(`  Prompt: ${trigger.prompt}`);
    }
  } else {
    console.log('No chain triggers detected.');
  }
}
