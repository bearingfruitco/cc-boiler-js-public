#!/usr/bin/env python3
"""
API Documentation Automation
Automatically generates OpenAPI specifications and interactive documentation
Part of v4.0 automation plan - Issue #21
"""

import os
import json
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any

class APIDocumentationGenerator:
    def __init__(self):
        self.openapi_dir = Path('.claude/api-docs/openapi')
        self.openapi_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_api_info(self, content: str, path: str) -> Dict[str, Any]:
        """Extract API information from route handler"""
        api_info = {
            'path': self._extract_api_path(path),
            'methods': [],
            'description': '',
            'parameters': [],
            'requestBody': None,
            'responses': {},
            'security': [],
            'tags': []
        }
        
        # Extract HTTP methods
        method_pattern = r'export\s+async\s+function\s+(GET|POST|PUT|DELETE|PATCH)'
        for match in re.finditer(method_pattern, content):
            api_info['methods'].append(match.group(1))
        
        # Extract parameters from URL
        if '{' in api_info['path'] or '[' in path:
            api_info['parameters'].extend(self._extract_path_params(path))
        
        # Extract query parameters
        if 'searchParams' in content or 'query' in content:
            api_info['parameters'].extend(self._extract_query_params(content))
        
        # Extract request body schema
        if any(method in api_info['methods'] for method in ['POST', 'PUT', 'PATCH']):
            api_info['requestBody'] = self._extract_request_body(content)
        
        # Extract response schemas
        api_info['responses'] = self._extract_responses(content)
        
        # Extract security requirements
        if 'auth' in content.lower() or 'session' in content:
            api_info['security'] = [{'bearerAuth': []}]
        
        # Extract tags from path
        api_info['tags'] = self._extract_tags(path)
        
        return api_info
    
    def _extract_api_path(self, file_path: str) -> str:
        """Convert file path to API path"""
        # app/api/users/[id]/route.ts -> /api/users/{id}
        path = file_path.replace('app/', '/').replace('/route.ts', '').replace('/route.js', '')
        path = re.sub(r'\[([^\]]+)\]', r'{\1}', path)
        return path
    
    def _extract_path_params(self, path: str) -> List[Dict]:
        """Extract path parameters"""
        params = []
        # Match [param] or {param} patterns
        pattern = r'[\[{]([^\]}]+)[\]}]'
        for match in re.finditer(pattern, path):
            param_name = match.group(1)
            params.append({
                'name': param_name,
                'in': 'path',
                'required': True,
                'schema': {'type': 'string'},
                'description': f'{param_name} parameter'
            })
        return params
    
    def _extract_query_params(self, content: str) -> List[Dict]:
        """Extract query parameters from code"""
        params = []
        # Look for searchParams.get() patterns
        pattern = r'searchParams\.get\([\'"](\w+)[\'"]\)'
        for match in re.finditer(pattern, content):
            param_name = match.group(1)
            params.append({
                'name': param_name,
                'in': 'query',
                'required': False,
                'schema': {'type': 'string'},
                'description': f'{param_name} query parameter'
            })
        return params
    
    def _extract_request_body(self, content: str) -> Dict:
        """Extract request body schema"""
        # Look for zod schemas
        schema_pattern = r'const\s+\w+Schema\s*=\s*z\.object\({([^}]+)}\)'
        match = re.search(schema_pattern, content, re.DOTALL)
        
        if match:
            schema_content = match.group(1)
            return {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': self._parse_zod_schema(schema_content)
                    }
                }
            }
        
        # Default request body
        return {
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {}
                    }
                }
            }
        }
    
    def _parse_zod_schema(self, schema_content: str) -> Dict:
        """Parse Zod schema to OpenAPI schema"""
        schema = {
            'type': 'object',
            'properties': {},
            'required': []
        }
        
        # Parse each field
        field_pattern = r'(\w+):\s*z\.(\w+)\((.*?)\)'
        for match in re.finditer(field_pattern, schema_content):
            field_name = match.group(1)
            field_type = match.group(2)
            
            # Map Zod types to OpenAPI types
            type_mapping = {
                'string': 'string',
                'number': 'number',
                'boolean': 'boolean',
                'object': 'object',
                'array': 'array'
            }
            
            schema['properties'][field_name] = {
                'type': type_mapping.get(field_type, 'string')
            }
            
            # Check if required
            if '.optional()' not in match.group(0):
                schema['required'].append(field_name)
        
        return schema
    
    def _extract_responses(self, content: str) -> Dict:
        """Extract response schemas"""
        responses = {
            '200': {
                'description': 'Successful response',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {}
                        }
                    }
                }
            }
        }
        
        # Look for NextResponse patterns
        response_pattern = r'NextResponse\.json\(([^)]+)\)'
        matches = list(re.finditer(response_pattern, content))
        
        if matches:
            # Try to extract response structure
            for match in matches:
                response_content = match.group(1)
                if '{' in response_content:
                    # Attempt to parse response structure
                    responses['200']['content']['application/json']['examples'] = {
                        'default': {
                            'value': '// Response data'
                        }
                    }
        
        # Look for error responses
        if '400' in content or 'BadRequest' in content:
            responses['400'] = {
                'description': 'Bad request',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'error': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        
        if '401' in content or 'Unauthorized' in content:
            responses['401'] = {
                'description': 'Unauthorized',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'error': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        
        return responses
    
    def _extract_tags(self, path: str) -> List[str]:
        """Extract tags from API path"""
        parts = path.split('/')
        tags = []
        
        for part in parts:
            if part and part != 'api' and not part.startswith('{'):
                tags.append(part.capitalize())
        
        return tags[:1]  # Use first meaningful part as tag
    
    def generate_openapi_spec(self, api_info: Dict, existing_spec: Dict = None) -> Dict:
        """Generate or update OpenAPI specification"""
        if existing_spec is None:
            existing_spec = {
                'openapi': '3.0.0',
                'info': {
                    'title': 'API Documentation',
                    'version': '1.0.0',
                    'description': 'Auto-generated API documentation'
                },
                'servers': [
                    {
                        'url': 'http://localhost:3000',
                        'description': 'Development server'
                    }
                ],
                'components': {
                    'securitySchemes': {
                        'bearerAuth': {
                            'type': 'http',
                            'scheme': 'bearer',
                            'bearerFormat': 'JWT'
                        }
                    }
                },
                'paths': {}
            }
        
        # Add or update path
        path = api_info['path']
        if path not in existing_spec['paths']:
            existing_spec['paths'][path] = {}
        
        # Add methods
        for method in api_info['methods']:
            existing_spec['paths'][path][method.lower()] = {
                'summary': f'{method} {path}',
                'description': api_info['description'] or f'{method} operation for {path}',
                'tags': api_info['tags'],
                'parameters': api_info['parameters'],
                'responses': api_info['responses']
            }
            
            if api_info['requestBody'] and method in ['POST', 'PUT', 'PATCH']:
                existing_spec['paths'][path][method.lower()]['requestBody'] = api_info['requestBody']
            
            if api_info['security']:
                existing_spec['paths'][path][method.lower()]['security'] = api_info['security']
        
        return existing_spec
    
    def generate_client_sdk(self, openapi_spec: Dict) -> str:
        """Generate TypeScript client SDK from OpenAPI spec"""
        sdk_content = """// Auto-generated API Client
import { z } from 'zod';

export class APIClient {
  private baseURL: string;
  private headers: Record<string, string>;
  
  constructor(baseURL = '/api', token?: string) {
    this.baseURL = baseURL;
    this.headers = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      this.headers['Authorization'] = `Bearer ${token}`;
    }
  }
  
  private async request<T>(
    method: string,
    path: string,
    options?: {
      params?: Record<string, string>;
      body?: any;
    }
  ): Promise<T> {
    const url = new URL(`${this.baseURL}${path}`, window.location.origin);
    
    if (options?.params) {
      Object.entries(options.params).forEach(([key, value]) => {
        url.searchParams.append(key, value);
      });
    }
    
    const response = await fetch(url.toString(), {
      method,
      headers: this.headers,
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    return response.json();
  }
"""
        
        # Generate methods for each endpoint
        for path, methods in openapi_spec['paths'].items():
            for method, operation in methods.items():
                sdk_content += self._generate_sdk_method(path, method, operation)
        
        sdk_content += "}\n"
        return sdk_content
    
    def _generate_sdk_method(self, path: str, method: str, operation: Dict) -> str:
        """Generate SDK method for an endpoint"""
        # Convert path to method name
        method_name = self._path_to_method_name(path, method)
        
        # Extract parameters
        path_params = [p for p in operation.get('parameters', []) if p['in'] == 'path']
        query_params = [p for p in operation.get('parameters', []) if p['in'] == 'query']
        
        # Build method signature
        params = []
        if path_params:
            for param in path_params:
                params.append(f"{param['name']}: string")
        
        if query_params:
            params.append("query?: { " + ", ".join([f"{p['name']}?: string" for p in query_params]) + " }")
        
        if operation.get('requestBody'):
            params.append("body: any")
        
        param_str = ", ".join(params)
        
        # Build path with replacements
        api_path = path
        for param in path_params:
            api_path = api_path.replace(f"{{{param['name']}}}", f"${{{param['name']}}}")
        
        return f"""
  async {method_name}({param_str}): Promise<any> {{
    return this.request('{method.upper()}', `{api_path}`{', { params: query, body }' if query_params or operation.get('requestBody') else ''});
  }}
"""
    
    def _path_to_method_name(self, path: str, method: str) -> str:
        """Convert API path to method name"""
        # /api/users/{id} -> getUsers or getUserById
        parts = path.split('/')[2:]  # Skip /api/
        name_parts = []
        
        for part in parts:
            if part and not part.startswith('{'):
                name_parts.append(part.capitalize())
            elif part.startswith('{'):
                name_parts.append('By' + part[1:-1].capitalize())
        
        return method.lower() + ''.join(name_parts)

def check_for_api_creation(tool_use):
    """Check if creating an API route"""
    if tool_use.tool != 'str_replace_editor':
        return False
    
    path = tool_use.path or ''
    
    # Check for API route patterns
    return ('app/api/' in path or 'pages/api/' in path) and path.endswith(('.ts', '.js'))

def main(tool_use):
    if not check_for_api_creation(tool_use):
        return
    
    path = tool_use.path
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    
    # Skip if opted out
    if '--no-api-docs' in content:
        return
    
    print(f"\n📚 AUTO-GENERATING API DOCUMENTATION")
    print(f"   API Route: {path}")
    
    generator = APIDocumentationGenerator()
    
    # Extract API information
    api_info = generator.extract_api_info(content, path)
    
    # Load existing OpenAPI spec
    openapi_path = generator.openapi_dir / 'openapi.json'
    existing_spec = {}
    if openapi_path.exists():
        with open(openapi_path) as f:
            existing_spec = json.load(f)
    
    # Generate or update OpenAPI spec
    openapi_spec = generator.generate_openapi_spec(api_info, existing_spec)
    
    # Save OpenAPI spec
    with open(openapi_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"✅ Updated OpenAPI spec: {openapi_path}")
    
    # Also save as YAML for better readability
    yaml_path = generator.openapi_dir / 'openapi.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(openapi_spec, f, default_flow_style=False)
    
    print(f"✅ Updated OpenAPI YAML: {yaml_path}")
    
    # Generate client SDK
    sdk_content = generator.generate_client_sdk(openapi_spec)
    sdk_path = Path('lib/api/client.generated.ts')
    sdk_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(sdk_path, 'w') as f:
        f.write(sdk_content)
    
    print(f"✅ Generated TypeScript SDK: {sdk_path}")
    
    # Generate Swagger UI setup
    swagger_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {{
      SwaggerUIBundle({{
        url: '/api/openapi.json',
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      }});
    }}
  </script>
</body>
</html>"""
    
    swagger_path = Path('public/api-docs.html')
    with open(swagger_path, 'w') as f:
        f.write(swagger_html)
    
    print(f"✅ Generated Swagger UI: {swagger_path}")
    print("\n📝 Access interactive API docs at: http://localhost:3000/api-docs.html")

if __name__ == "__main__":
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    class ToolUse:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
