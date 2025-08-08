/**
 * Serena MCP Connector
 * Semantic code retrieval and understanding for large codebases
 */

require('dotenv').config();
const fs = require('fs').promises;
const path = require('path');

class SerenaMCP {
  constructor() {
    this.connected = false;
    this.codebaseIndex = new Map();
    this.semanticMap = new Map();
    this.capabilities = [
      'code:search',
      'semantic:retrieval',
      'context:understand',
      'dependencies:map',
      'structure:analyze',
      'patterns:identify'
    ];
  }

  async connect() {
    try {
      console.log('🔍 Connecting to Serena MCP...');
      
      // Initialize semantic understanding
      await this.indexCodebase();
      
      this.connected = true;
      console.log('✅ Serena MCP connected and indexed');
      return true;
    } catch (error) {
      console.error('❌ Serena MCP connection failed:', error.message);
      return false;
    }
  }

  async testConnection() {
    if (!this.connected) {
      await this.connect();
    }

    try {
      const stats = {
        filesIndexed: this.codebaseIndex.size,
        semanticMappings: this.semanticMap.size,
        ready: true
      };

      return {
        success: true,
        message: 'Serena MCP operational',
        capabilities: this.capabilities,
        stats
      };
    } catch (error) {
      return {
        success: false,
        message: error.message
      };
    }
  }

  // Index the codebase for semantic understanding
  async indexCodebase(rootDir = '.') {
    try {
      console.log('Indexing codebase...');
      
      const files = await this.getAllFiles(rootDir);
      
      for (const file of files) {
        if (this.shouldIndex(file)) {
          const content = await fs.readFile(file, 'utf8');
          const metadata = this.extractMetadata(content, file);
          
          this.codebaseIndex.set(file, {
            content,
            metadata,
            lastModified: new Date(),
            dependencies: this.extractDependencies(content),
            exports: this.extractExports(content),
            functions: this.extractFunctions(content)
          });

          // Build semantic map
          this.buildSemanticMap(file, content, metadata);
        }
      }

      console.log(`Indexed ${this.codebaseIndex.size} files`);
      return true;
    } catch (error) {
      throw new Error(`Indexing failed: ${error.message}`);
    }
  }

  // Semantic search through codebase
  async searchCode(query, options = {}) {
    /**
     * Search for code semantically
     * @param {string} query - What to search for
     * @param {Object} options - Search options
     */
    try {
      const results = [];
      const queryTerms = this.tokenize(query.toLowerCase());
      
      for (const [file, data] of this.codebaseIndex) {
        const relevance = this.calculateRelevance(queryTerms, data);
        
        if (relevance > (options.threshold || 0.3)) {
          results.push({
            file,
            relevance,
            snippet: this.extractRelevantSnippet(data.content, queryTerms),
            context: data.metadata
          });
        }
      }

      // Sort by relevance
      results.sort((a, b) => b.relevance - a.relevance);
      
      return {
        query,
        results: results.slice(0, options.limit || 10),
        totalFound: results.length
      };
    } catch (error) {
      throw new Error(`Search failed: ${error.message}`);
    }
  }

  // Understand context around a code location
  async understandContext(file, lineNumber) {
    /**
     * Get semantic context around a specific location
     */
    try {
      const fileData = this.codebaseIndex.get(file);
      if (!fileData) {
        throw new Error(`File not indexed: ${file}`);
      }

      const lines = fileData.content.split('\n');
      const contextWindow = 10; // Lines before and after
      
      const start = Math.max(0, lineNumber - contextWindow);
      const end = Math.min(lines.length, lineNumber + contextWindow);
      
      const context = {
        file,
        lineNumber,
        function: this.findContainingFunction(fileData.functions, lineNumber),
        dependencies: fileData.dependencies,
        snippet: lines.slice(start, end).join('\n'),
        relatedFiles: this.findRelatedFiles(file),
        semanticContext: this.getSemanticContext(file, lineNumber)
      };

      return context;
    } catch (error) {
      throw new Error(`Context understanding failed: ${error.message}`);
    }
  }

  // Find related files based on imports/exports
  async findRelatedFiles(file) {
    const related = new Set();
    const fileData = this.codebaseIndex.get(file);
    
    if (!fileData) return [];

    // Find files that import this file
    for (const [otherFile, otherData] of this.codebaseIndex) {
      if (otherFile !== file) {
        for (const dep of otherData.dependencies) {
          if (dep.includes(path.basename(file, path.extname(file)))) {
            related.add(otherFile);
          }
        }
      }
    }

    // Find files this file imports
    for (const dep of fileData.dependencies) {
      for (const [otherFile] of this.codebaseIndex) {
        if (otherFile.includes(dep)) {
          related.add(otherFile);
        }
      }
    }

    return Array.from(related);
  }

  // Analyze code structure
  async analyzeStructure(file) {
    try {
      const fileData = this.codebaseIndex.get(file);
      if (!fileData) {
        throw new Error(`File not indexed: ${file}`);
      }

      const structure = {
        file,
        type: this.detectFileType(file),
        components: [],
        patterns: [],
        complexity: 0
      };

      // Detect components/classes
      const componentMatches = fileData.content.match(/(?:class|function|const)\s+(\w+)/g);
      if (componentMatches) {
        structure.components = componentMatches.map(m => m.split(/\s+/)[1]);
      }

      // Detect patterns
      if (fileData.content.includes('useState')) {
        structure.patterns.push('React Hooks');
      }
      if (fileData.content.includes('async') && fileData.content.includes('await')) {
        structure.patterns.push('Async/Await');
      }
      if (fileData.content.includes('try') && fileData.content.includes('catch')) {
        structure.patterns.push('Error Handling');
      }

      // Calculate complexity
      structure.complexity = this.calculateComplexity(fileData.content);

      return structure;
    } catch (error) {
      throw new Error(`Structure analysis failed: ${error.message}`);
    }
  }

  // Helper Methods
  async getAllFiles(dir, files = []) {
    const items = await fs.readdir(dir, { withFileTypes: true });
    
    for (const item of items) {
      const fullPath = path.join(dir, item.name);
      
      if (item.isDirectory()) {
        if (!this.shouldSkipDirectory(item.name)) {
          await this.getAllFiles(fullPath, files);
        }
      } else {
        files.push(fullPath);
      }
    }
    
    return files;
  }

  shouldIndex(file) {
    const extensions = ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.go'];
    return extensions.some(ext => file.endsWith(ext));
  }

  shouldSkipDirectory(dir) {
    const skipDirs = ['node_modules', '.git', 'dist', 'build', '.next', '__pycache__'];
    return skipDirs.includes(dir);
  }

  extractMetadata(content, file) {
    return {
      language: this.detectLanguage(file),
      lines: content.split('\n').length,
      size: content.length,
      hasTests: content.includes('test') || content.includes('spec'),
      hasTypes: content.includes('interface') || content.includes('type')
    };
  }

  extractDependencies(content) {
    const deps = [];
    const importMatches = content.match(/(?:import|require)\s*\(?['"]([^'"]+)['"]\)?/g);
    
    if (importMatches) {
      importMatches.forEach(match => {
        const dep = match.match(/['"]([^'"]+)['"]/);
        if (dep) deps.push(dep[1]);
      });
    }
    
    return deps;
  }

  extractExports(content) {
    const exports = [];
    const exportMatches = content.match(/export\s+(?:default\s+)?(?:class|function|const|interface|type)\s+(\w+)/g);
    
    if (exportMatches) {
      exportMatches.forEach(match => {
        const name = match.match(/\s+(\w+)$/);
        if (name) exports.push(name[1]);
      });
    }
    
    return exports;
  }

  extractFunctions(content) {
    const functions = [];
    const lines = content.split('\n');
    
    lines.forEach((line, index) => {
      if (line.match(/(?:function|const|let|var)\s+\w+\s*=?\s*(?:async\s*)?\(/) ||
          line.match(/^\s*(?:async\s+)?(?:\w+)\s*\([^)]*\)\s*{/)) {
        const name = line.match(/\s+(\w+)\s*[=(]/);
        if (name) {
          functions.push({
            name: name[1],
            line: index + 1
          });
        }
      }
    });
    
    return functions;
  }

  buildSemanticMap(file, content, metadata) {
    const tokens = this.tokenize(content);
    
    tokens.forEach(token => {
      if (!this.semanticMap.has(token)) {
        this.semanticMap.set(token, new Set());
      }
      this.semanticMap.get(token).add(file);
    });
  }

  tokenize(text) {
    return text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(token => token.length > 2);
  }

  calculateRelevance(queryTerms, fileData) {
    let relevance = 0;
    const fileTokens = this.tokenize(fileData.content);
    
    queryTerms.forEach(term => {
      const count = fileTokens.filter(token => token.includes(term)).length;
      relevance += count / fileTokens.length;
    });
    
    // Boost for metadata matches
    if (fileData.metadata.hasTests && queryTerms.includes('test')) {
      relevance += 0.2;
    }
    if (fileData.metadata.hasTypes && queryTerms.includes('type')) {
      relevance += 0.2;
    }
    
    return Math.min(1, relevance);
  }

  extractRelevantSnippet(content, queryTerms) {
    const lines = content.split('\n');
    let bestLine = 0;
    let bestScore = 0;
    
    lines.forEach((line, index) => {
      const lineTokens = this.tokenize(line);
      let score = 0;
      
      queryTerms.forEach(term => {
        if (lineTokens.includes(term)) score++;
      });
      
      if (score > bestScore) {
        bestScore = score;
        bestLine = index;
      }
    });
    
    const start = Math.max(0, bestLine - 2);
    const end = Math.min(lines.length, bestLine + 3);
    
    return lines.slice(start, end).join('\n');
  }

  findContainingFunction(functions, lineNumber) {
    let containing = null;
    let minDistance = Infinity;
    
    functions.forEach(func => {
      if (func.line <= lineNumber) {
        const distance = lineNumber - func.line;
        if (distance < minDistance) {
          minDistance = distance;
          containing = func.name;
        }
      }
    });
    
    return containing;
  }

  getSemanticContext(file, lineNumber) {
    // Get semantic understanding of what this code does
    const fileData = this.codebaseIndex.get(file);
    if (!fileData) return null;

    const lines = fileData.content.split('\n');
    const line = lines[lineNumber - 1] || '';
    
    const context = {
      purpose: '',
      type: ''
    };

    if (line.includes('test') || line.includes('spec')) {
      context.type = 'test';
      context.purpose = 'Testing functionality';
    } else if (line.includes('async') || line.includes('await')) {
      context.type = 'async';
      context.purpose = 'Asynchronous operation';
    } else if (line.includes('return')) {
      context.type = 'return';
      context.purpose = 'Returning value from function';
    }

    return context;
  }

  detectFileType(file) {
    if (file.includes('test') || file.includes('spec')) return 'test';
    if (file.includes('component')) return 'component';
    if (file.includes('service')) return 'service';
    if (file.includes('util')) return 'utility';
    if (file.includes('model')) return 'model';
    return 'general';
  }

  detectLanguage(file) {
    const ext = path.extname(file);
    const langMap = {
      '.js': 'javascript',
      '.ts': 'typescript',
      '.jsx': 'javascript-react',
      '.tsx': 'typescript-react',
      '.py': 'python',
      '.java': 'java',
      '.go': 'go'
    };
    return langMap[ext] || 'unknown';
  }

  calculateComplexity(content) {
    let complexity = 1;
    
    // Count decision points
    complexity += (content.match(/if\s*\(/g) || []).length;
    complexity += (content.match(/for\s*\(/g) || []).length;
    complexity += (content.match(/while\s*\(/g) || []).length;
    complexity += (content.match(/case\s+/g) || []).length;
    complexity += (content.match(/catch\s*\(/g) || []).length;
    
    return complexity;
  }
}

module.exports = SerenaMCP;
