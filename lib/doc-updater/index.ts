/**
 * Documentation Updater
 * 
 * Automatically updates documentation as code changes
 */

export * from './types';
export * from './analyzer';
export * from './generator';
export * from './updater';
export * from './watcher';

// Re-export main classes
export { DocumentationUpdater as default } from './updater';
export { DocumentationWatcher } from './watcher';
export { CodeAnalyzer } from './analyzer';
export { DocumentationGenerator } from './generator';
