#!/usr/bin/env python3
"""
API Documentation Automation
Automatically generates OpenAPI specifications and interactive documentation
Part of v4.0 automation plan - Issue #21
"""

import sys
import json
import re
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
            'tool_input': [],
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
            api_info['tool_input'].extend(self._extract_path_params(path))
        
        # Extract query parameters
        if 'searchParams' in content or 'query' in content:
            api_info['tool_input'].extend(self._extract_query_params(content))
        
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
                'tool_input': api_info['tool_input'],
                'responses': api_info['responses']
            }
            
            if api_info['requestBody'] and method in ['POST', 'PUT', 'PATCH']:
                existing_spec['paths'][path][method.lower()]['requestBody'] = api_info['requestBody']
            
            if api_info['security']:
                existing_spec['paths'][path][method.lower()]['security'] = api_info['security']
        
        return existing_spec

def check_for_api_creation(input_data):
    """Check if creating an API route"""
    tool_name = input_data.get('tool_name', '')
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return False
    
    tool_input = input_data.get('tool_input', {})
    path = tool_input.get('path', '') or tool_input.get('file_path', '')
    
    # Check for API route patterns
    return ('app/api/' in path or 'pages/api/' in path) and path.endswith(('.ts', '.js'))

def main():
    """Main hook logic"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        if not check_for_api_creation(input_data):
            sys.exit(0)
        
        tool_input = input_data.get('tool_input', {})
        tool_name = input_data.get('tool_name', '')
        path = tool_input.get('path', '') or tool_input.get('file_path', '')
        
        # Get content based on tool
        if tool_name == 'Write':
            content = tool_input.get('content', '')
        else:
            content = tool_input.get('new_str', '')
        
        # Skip if opted out
        if '--no-api-docs' in content:
            sys.exit(0)
        
        print(f"\n📚 AUTO-GENERATING API DOCUMENTATION", file=sys.stderr)
        print(f"   API Route: {path}", file=sys.stderr)
        
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
        
        print(f"✅ Updated OpenAPI spec: {openapi_path}", file=sys.stderr)
        
    except Exception as e:
        # Log error to stderr and continue
        print(f"API docs generator hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
