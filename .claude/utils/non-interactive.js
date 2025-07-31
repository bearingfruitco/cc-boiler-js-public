#!/usr/bin/env node

/**
 * Non-Interactive Mode Support for Claude Code
 * 
 * This module provides utilities for commands to support Claude Code's
 * --non-interactive flag for CI/CD automation.
 * 
 * Usage in commands:
 * const { isNonInteractive, exitWithResult } = require('.claude/utils/non-interactive.js');
 */

/**
 * Check if running in non-interactive mode
 * @returns {boolean} True if non-interactive mode is active
 */
function isNonInteractive() {
  // Claude Code sets this environment variable in non-interactive mode
  return process.env.CLAUDE_NON_INTERACTIVE === 'true';
}

/**
 * Exit with proper code and structured output for non-interactive mode
 * @param {boolean} success - Whether the operation was successful
 * @param {Object} result - Result data to output
 * @param {string} [message] - Optional message for interactive mode
 */
function exitWithResult(success, result, message) {
  if (isNonInteractive()) {
    // Non-interactive mode: output JSON and exit with code
    console.log(JSON.stringify({
      success,
      timestamp: new Date().toISOString(),
      ...result
    }, null, 2));
    process.exit(success ? 0 : 1);
  } else {
    // Interactive mode: show human-readable message
    if (message) {
      console.log(message);
    }
    if (!success) {
      process.exit(1);
    }
  }
}

/**
 * Format output based on mode
 * @param {string} interactiveOutput - Output for interactive mode
 * @param {Object} structuredOutput - Output for non-interactive mode
 */
function formatOutput(interactiveOutput, structuredOutput) {
  if (isNonInteractive()) {
    console.log(JSON.stringify(structuredOutput, null, 2));
  } else {
    console.log(interactiveOutput);
  }
}

/**
 * Skip confirmation prompts in non-interactive mode
 * @param {string} prompt - Confirmation prompt text
 * @param {boolean} defaultValue - Default value if non-interactive
 * @returns {Promise<boolean>} User response or default
 */
async function confirmAction(prompt, defaultValue = true) {
  if (isNonInteractive()) {
    return defaultValue;
  }
  
  // In interactive mode, would use readline or similar
  // For now, just return true for simplicity
  console.log(prompt + ' (y/n)');
  return true;
}

/**
 * Handle command execution with non-interactive support
 * @param {Function} commandFn - The command function to execute
 * @param {Object} options - Command options
 */
async function executeCommand(commandFn, options = {}) {
  try {
    const startTime = Date.now();
    const result = await commandFn(options);
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    exitWithResult(true, {
      ...result,
      duration_ms: duration
    }, result.message);
  } catch (error) {
    exitWithResult(false, {
      error: error.message,
      stack: isNonInteractive() ? error.stack : undefined
    }, `Error: ${error.message}`);
  }
}

module.exports = {
  isNonInteractive,
  exitWithResult,
  formatOutput,
  confirmAction,
  executeCommand
};
