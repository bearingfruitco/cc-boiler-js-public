import * as ts from 'typescript';
import * as path from 'path';
import { promises as fs } from 'fs';
import {
  ParsedComponent,
  PropDefinition,
  MethodDefinition,
  ParameterDefinition,
  APIEndpoint,
  FileChange,
  CodeChange,
  ChangeType
} from './types';

/**
 * Analyzes TypeScript/JavaScript files to extract documentation-relevant information
 */
export class CodeAnalyzer {
  private program: ts.Program | null = null;
  private checker: ts.TypeChecker | null = null;

  /**
   * Analyze a file and extract documentation information
   */
  async analyzeFile(filePath: string): Promise<FileChange> {
    const content = await fs.readFile(filePath, 'utf-8');
    const sourceFile = ts.createSourceFile(
      filePath,
      content,
      ts.ScriptTarget.Latest,
      true
    );

    const changes: CodeChange[] = [];
    const fileExt = path.extname(filePath);
    const language = this.getLanguageFromExt(fileExt);

    // Analyze based on file type
    if (filePath.includes('/components/')) {
      const components = this.analyzeComponents(sourceFile);
      changes.push(...this.componentsToChanges(components));
    } else if (filePath.includes('/api/')) {
      const endpoints = this.analyzeAPIRoutes(sourceFile, filePath);
      changes.push(...this.endpointsToChanges(endpoints));
    } else if (filePath.includes('/types/') || filePath.includes('.types.')) {
      const types = this.analyzeTypes(sourceFile);
      changes.push(...this.typesToChanges(types));
    } else {
      // General analysis
      const exports = this.analyzeExports(sourceFile);
      changes.push(...exports);
    }

    return {
      path: filePath,
      type: 'modified', // Would be determined by git status
      language,
      changes
    };
  }

  /**
   * Analyze React components
   */
  private analyzeComponents(sourceFile: ts.SourceFile): ParsedComponent[] {
    const components: ParsedComponent[] = [];

    ts.forEachChild(sourceFile, (node) => {
      // Function components
      if (ts.isFunctionDeclaration(node) && node.name && this.isComponent(node.name.text)) {
        components.push(this.parseFunctionComponent(node));
      }
      
      // Arrow function components
      if (ts.isVariableStatement(node)) {
        node.declarationList.declarations.forEach(decl => {
          if (ts.isIdentifier(decl.name) && this.isComponent(decl.name.text)) {
            if (decl.initializer && ts.isArrowFunction(decl.initializer)) {
              components.push(this.parseArrowComponent(decl));
            }
          }
        });
      }
    });

    return components;
  }

  /**
   * Parse function component
   */
  private parseFunctionComponent(node: ts.FunctionDeclaration): ParsedComponent {
    const name = node.name!.text;
    const jsDoc = this.getJSDoc(node);
    const props = this.extractProps(node.parameters[0]);

    return {
      name,
      type: 'function',
      props,
      description: jsDoc?.description,
      examples: jsDoc?.examples,
      exports: [name]
    };
  }

  /**
   * Parse arrow function component
   */
  private parseArrowComponent(node: ts.VariableDeclaration): ParsedComponent {
    const name = (node.name as ts.Identifier).text;
    const jsDoc = this.getJSDoc(node);
    const arrowFunc = node.initializer as ts.ArrowFunction;
    const props = this.extractProps(arrowFunc.parameters[0]);

    return {
      name,
      type: 'const',
      props,
      description: jsDoc?.description,
      examples: jsDoc?.examples,
      exports: [name]
    };
  }

  /**
   * Extract props from parameter
   */
  private extractProps(param?: ts.ParameterDeclaration): PropDefinition[] {
    if (!param || !param.type) return [];

    const props: PropDefinition[] = [];

    if (ts.isTypeLiteralNode(param.type)) {
      param.type.members.forEach(member => {
        if (ts.isPropertySignature(member) && member.name && ts.isIdentifier(member.name)) {
          props.push({
            name: member.name.text,
            type: member.type ? this.getTypeString(member.type) : 'any',
            required: !member.questionToken,
            description: this.getJSDoc(member)?.description
          });
        }
      });
    }

    return props;
  }

  /**
   * Analyze API routes (Next.js style)
   */
  private analyzeAPIRoutes(sourceFile: ts.SourceFile, filePath: string): APIEndpoint[] {
    const endpoints: APIEndpoint[] = [];
    const apiPath = this.getAPIPath(filePath);

    ts.forEachChild(sourceFile, (node) => {
      // Look for exported functions like GET, POST, etc.
      if (ts.isVariableStatement(node)) {
        const exportModifier = node.modifiers?.find(m => m.kind === ts.SyntaxKind.ExportKeyword);
        if (exportModifier) {
          node.declarationList.declarations.forEach(decl => {
            if (ts.isIdentifier(decl.name)) {
              const method = decl.name.text;
              if (['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
                endpoints.push(this.parseAPIEndpoint(apiPath, method, decl));
              }
            }
          });
        }
      }
    });

    return endpoints;
  }

  /**
   * Parse API endpoint
   */
  private parseAPIEndpoint(path: string, method: string, node: ts.VariableDeclaration): APIEndpoint {
    const jsDoc = this.getJSDoc(node);

    return {
      path,
      method,
      description: jsDoc?.description,
      parameters: this.extractAPIParams(jsDoc),
      responses: this.extractAPIResponses(jsDoc),
      authentication: jsDoc?.tags?.some(tag => tag.name === 'authenticated')
    };
  }

  /**
   * Analyze type definitions
   */
  private analyzeTypes(sourceFile: ts.SourceFile): any[] {
    const types: any[] = [];

    ts.forEachChild(sourceFile, (node) => {
      if (ts.isInterfaceDeclaration(node) || ts.isTypeAliasDeclaration(node)) {
        const jsDoc = this.getJSDoc(node);
        types.push({
          name: node.name.text,
          kind: ts.isInterfaceDeclaration(node) ? 'interface' : 'type',
          description: jsDoc?.description,
          exported: this.isExported(node)
        });
      }
    });

    return types;
  }

  /**
   * Analyze general exports
   */
  private analyzeExports(sourceFile: ts.SourceFile): CodeChange[] {
    const changes: CodeChange[] = [];

    ts.forEachChild(sourceFile, (node) => {
      if (ts.isExportDeclaration(node) || ts.isExportAssignment(node)) {
        // Handle export statements
      } else if (node.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword)) {
        // Handle exported declarations
        if (ts.isFunctionDeclaration(node) && node.name) {
          changes.push({
            type: ChangeType.FUNCTION_ADDED,
            name: node.name.text,
            signature: this.getFunctionSignature(node),
            description: this.getJSDoc(node)?.description
          });
        }
      }
    });

    return changes;
  }

  /**
   * Helper methods
   */

  private isComponent(name: string): boolean {
    return /^[A-Z]/.test(name);
  }

  private getJSDoc(node: ts.Node): any {
    const jsDocNodes = ts.getJSDocCommentsAndTags(node);
    if (jsDocNodes.length === 0) return null;

    const jsDoc = jsDocNodes[0];
    if (!ts.isJSDoc(jsDoc)) return null;

    return {
      description: jsDoc.comment ? this.getTextFromJSDocComment(jsDoc.comment) : undefined,
      tags: jsDoc.tags?.map(tag => ({
        name: tag.tagName.text,
        text: tag.comment ? this.getTextFromJSDocComment(tag.comment) : undefined
      })),
      examples: this.extractExamples(jsDoc)
    };
  }

  private getTextFromJSDocComment(comment: string | ts.NodeArray<ts.JSDocComment>): string {
    if (typeof comment === 'string') return comment;
    return comment.map(c => c.text).join('');
  }

  private extractExamples(jsDoc: ts.JSDoc): string[] {
    const examples: string[] = [];
    jsDoc.tags?.forEach(tag => {
      if (tag.tagName.text === 'example' && tag.comment) {
        examples.push(this.getTextFromJSDocComment(tag.comment));
      }
    });
    return examples;
  }

  private getTypeString(type: ts.TypeNode): string {
    // Simplified type string extraction
    return type.getText();
  }

  private isExported(node: ts.Declaration): boolean {
    return node.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword) || false;
  }

  private getFunctionSignature(func: ts.FunctionDeclaration): string {
    const params = func.parameters.map(p => `${p.name?.getText()}: ${p.type?.getText() || 'any'}`).join(', ');
    const returnType = func.type?.getText() || 'void';
    return `(${params}): ${returnType}`;
  }

  private getAPIPath(filePath: string): string {
    // Extract API path from file path (Next.js convention)
    const match = filePath.match(/app\/api\/(.+?)\/route\.(ts|js)/);
    if (match) {
      return `/api/${match[1]}`;
    }
    return '/api/unknown';
  }

  private extractAPIParams(jsDoc: any): any[] {
    // Extract parameters from JSDoc @param tags
    const params: any[] = [];
    jsDoc?.tags?.forEach((tag: any) => {
      if (tag.name === 'param') {
        // Parse param tag
      }
    });
    return params;
  }

  private extractAPIResponses(jsDoc: any): any[] {
    // Extract responses from JSDoc @returns tags
    return [
      {
        status: 200,
        description: 'Success'
      }
    ];
  }

  private getLanguageFromExt(ext: string): string {
    const langMap: Record<string, string> = {
      '.ts': 'typescript',
      '.tsx': 'typescript',
      '.js': 'javascript',
      '.jsx': 'javascript'
    };
    return langMap[ext] || 'unknown';
  }

  private componentsToChanges(components: ParsedComponent[]): CodeChange[] {
    return components.map(comp => ({
      type: ChangeType.CLASS_ADDED,
      name: comp.name,
      description: comp.description,
      metadata: {
        props: comp.props,
        examples: comp.examples
      }
    }));
  }

  private endpointsToChanges(endpoints: APIEndpoint[]): CodeChange[] {
    return endpoints.map(endpoint => ({
      type: ChangeType.API_ENDPOINT_ADDED,
      name: `${endpoint.method} ${endpoint.path}`,
      description: endpoint.description,
      metadata: {
        parameters: endpoint.parameters,
        responses: endpoint.responses,
        authentication: endpoint.authentication
      }
    }));
  }

  private typesToChanges(types: any[]): CodeChange[] {
    return types.map(type => ({
      type: ChangeType.TYPE_ADDED,
      name: type.name,
      description: type.description,
      metadata: {
        kind: type.kind,
        exported: type.exported
      }
    }));
  }
}
