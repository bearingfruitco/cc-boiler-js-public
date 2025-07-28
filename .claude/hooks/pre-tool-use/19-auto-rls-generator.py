#!/usr/bin/env python3
"""
Auto RLS Generator
Automatically generates Supabase RLS policies from API requirements
"""

import os
import json
import re
from pathlib import Path

def extract_data_requirements(content):
    """Extract data access patterns from API code"""
    patterns = {
        'select': [],
        'insert': [],
        'update': [],
        'delete': []
    }
    
    # Find Supabase queries
    select_pattern = r'\.from\([\'"](\w+)[\'"]\)\.select'
    insert_pattern = r'\.from\([\'"](\w+)[\'"]\)\.insert'
    update_pattern = r'\.from\([\'"](\w+)[\'"]\)\.update'
    delete_pattern = r'\.from\([\'"](\w+)[\'"]\)\.delete'
    
    for match in re.finditer(select_pattern, content):
        patterns['select'].append(match.group(1))
    for match in re.finditer(insert_pattern, content):
        patterns['insert'].append(match.group(1))
    for match in re.finditer(update_pattern, content):
        patterns['update'].append(match.group(1))
    for match in re.finditer(delete_pattern, content):
        patterns['delete'].append(match.group(1))
    
    return patterns

def generate_rls_policies(table, operations, api_name):
    """Generate RLS policies based on operations"""
    policies = []
    
    # Determine auth requirements
    auth_required = 'auth.uid()' in operations.get('context', '')
    
    for operation in operations:
        if operation == 'select':
            if auth_required:
                policy = f"""
-- Policy: {api_name}_select_{table}
CREATE POLICY "{api_name}_select_{table}" ON {table}
FOR SELECT
USING (
    auth.uid() IS NOT NULL
    AND (
        -- User owns the record
        auth.uid() = user_id
        -- OR user has permission
        OR EXISTS (
            SELECT 1 FROM user_permissions
            WHERE user_id = auth.uid()
            AND resource = '{table}'
            AND action = 'read'
        )
    )
);"""
            else:
                policy = f"""
-- Policy: {api_name}_select_{table}
CREATE POLICY "{api_name}_select_{table}" ON {table}
FOR SELECT
USING (true); -- Public read (review if this is intended)"""
            
            policies.append(policy)
        
        elif operation == 'insert':
            policy = f"""
-- Policy: {api_name}_insert_{table}
CREATE POLICY "{api_name}_insert_{table}" ON {table}
FOR INSERT
WITH CHECK (
    auth.uid() IS NOT NULL
    AND auth.uid() = user_id
);"""
            policies.append(policy)
        
        elif operation == 'update':
            policy = f"""
-- Policy: {api_name}_update_{table}
CREATE POLICY "{api_name}_update_{table}" ON {table}
FOR UPDATE
USING (
    auth.uid() IS NOT NULL
    AND auth.uid() = user_id
)
WITH CHECK (
    auth.uid() IS NOT NULL
    AND auth.uid() = user_id
);"""
            policies.append(policy)
        
        elif operation == 'delete':
            policy = f"""
-- Policy: {api_name}_delete_{table}
CREATE POLICY "{api_name}_delete_{table}" ON {table}
FOR DELETE
USING (
    auth.uid() IS NOT NULL
    AND (
        auth.uid() = user_id
        OR EXISTS (
            SELECT 1 FROM user_permissions
            WHERE user_id = auth.uid()
            AND resource = '{table}'
            AND action = 'delete'
        )
    )
);"""
            policies.append(policy)
    
    return policies

def generate_permission_matrix(tables, operations):
    """Generate a permission matrix for the API"""
    matrix = {
        "api_permissions": {
            "authenticated": {},
            "anonymous": {},
            "admin": {}
        }
    }
    
    for table in tables:
        for role in matrix["api_permissions"]:
            if role == "admin":
                # Admins get all permissions
                matrix["api_permissions"][role][table] = ["select", "insert", "update", "delete"]
            elif role == "authenticated":
                # Authenticated users get limited permissions
                matrix["api_permissions"][role][table] = operations.get(table, [])
            else:
                # Anonymous users get very limited permissions
                if "public" in table or not operations.get('auth_required', True):
                    matrix["api_permissions"][role][table] = ["select"]
                else:
                    matrix["api_permissions"][role][table] = []
    
    return matrix

def generate_security_tests(api_name, tables, operations):
    """Generate security tests for the API"""
    tests = f"""
import {{ describe, test, expect }} from '@jest/globals';
import {{ createClient }} from '@supabase/supabase-js';
import {{ setupTestUser, cleanupTestUser }} from '@/lib/test-utils';

describe('Security: {api_name} API', () => {{
    let authenticatedClient;
    let anonymousClient;
    let testUser;
    
    beforeAll(async () => {{
        testUser = await setupTestUser();
        authenticatedClient = createClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
            {{ auth: {{ persistSession: false }} }}
        );
        await authenticatedClient.auth.setSession(testUser.session);
        
        anonymousClient = createClient(
            process.env.NEXT_PUBLIC_SUPABASE_URL!,
            process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
        );
    }});
    
    afterAll(async () => {{
        await cleanupTestUser(testUser);
    }});
"""
    
    for table in tables:
        tests += f"""
    
    describe('{table} table security', () => {{
        test('authenticated user can access own records', async () => {{
            const {{ data, error }} = await authenticatedClient
                .from('{table}')
                .select()
                .eq('user_id', testUser.id);
            
            expect(error).toBeNull();
        }});
        
        test('anonymous user cannot access protected records', async () => {{
            const {{ data, error }} = await anonymousClient
                .from('{table}')
                .select();
            
            expect(error).not.toBeNull();
            expect(error.code).toBe('PGRST301');
        }});
        
        test('user cannot access other users records', async () => {{
            const {{ data, error }} = await authenticatedClient
                .from('{table}')
                .select()
                .eq('user_id', 'other-user-id');
            
            expect(data).toEqual([]);
        }});
    }});
"""
    
    tests += "\n});\n"
    return tests

def main(tool_use):
    # Only process if creating API files
    if tool_use.tool != 'str_replace_editor' or not tool_use.path:
        return
    
    if 'api/' not in tool_use.path or not tool_use.path.endswith('.ts'):
        return
    
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    api_name = Path(tool_use.path).stem
    
    # Extract data requirements
    data_patterns = extract_data_requirements(content)
    if not any(data_patterns.values()):
        return  # No database operations
    
    # Get unique tables
    all_tables = set()
    for ops in data_patterns.values():
        all_tables.update(ops)
    
    if not all_tables:
        return
    
    print(f"\n🔒 Auto-generating RLS policies for {api_name} API...")
    
    # Create security directory
    security_dir = Path('.claude/security/policies')
    security_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate RLS policies
    all_policies = []
    for table in all_tables:
        operations = [op for op, tables in data_patterns.items() if table in tables]
        policies = generate_rls_policies(table, operations, api_name)
        all_policies.extend(policies)
    
    # Write RLS policies
    policy_file = security_dir / f"{api_name}.sql"
    with open(policy_file, 'w') as f:
        f.write(f"-- Auto-generated RLS policies for {api_name} API\n")
        f.write("-- Review and modify as needed\n\n")
        f.write("\n\n".join(all_policies))
    
    print(f"✅ Created RLS policies: {policy_file}")
    
    # Generate permission matrix
    matrix = generate_permission_matrix(all_tables, data_patterns)
    matrix_file = security_dir.parent / 'rules' / f"{api_name}.json"
    matrix_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(matrix_file, 'w') as f:
        json.dump(matrix, f, indent=2)
    
    print(f"✅ Created permission matrix: {matrix_file}")
    
    # Generate security tests
    tests = generate_security_tests(api_name, all_tables, data_patterns)
    test_dir = Path('tests/security')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_file = test_dir / f"{api_name}.security.test.ts"
    with open(test_file, 'w') as f:
        f.write(tests)
    
    print(f"✅ Created security tests: {test_file}")
    print("\n📝 Next steps:")
    print("1. Review generated RLS policies")
    print("2. Run security tests: pnpm test:security")
    print("3. Deploy policies: pnpm db:push")

if __name__ == "__main__":
    import json
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    class ToolUse:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
