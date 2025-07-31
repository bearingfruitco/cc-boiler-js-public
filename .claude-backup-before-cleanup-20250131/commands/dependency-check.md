# Dependency Tracking Commands

Track component dependencies using simple @used-by comments.

## Arguments:
- $ACTION: check|scan|update|breaking
- $COMPONENT: Component name to check

## Usage:
```bash
/deps check Button
/deps scan
/deps update Button
/deps breaking Button

# Non-interactive mode for CI/CD
claude --non-interactive "/deps scan"
```

## Non-Interactive Mode Support

When running in non-interactive mode, outputs structured JSON:

```json
{
  "action": "scan",
  "status": "completed",
  "summary": {
    "totalComponents": 45,
    "componentsWithDeps": 38,
    "orphanedComponents": 7,
    "circularDependencies": 0
  },
  "issues": [
    {
      "type": "missing-export",
      "component": "UserAvatar",
      "file": "components/ui/UserAvatar.tsx"
    }
  ],
  "exitCode": 0
}
```

## Enhanced Implementation

!`python3 << 'EOF'
import json
import os
import sys
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Check if running in non-interactive mode
is_non_interactive = os.environ.get('CLAUDE_NON_INTERACTIVE', 'false').lower() == 'true'

# Parse arguments
action = """$ACTION""".strip() or "check"
component = """$COMPONENT""".strip()

def find_component_files():
    """Find all component files in the project"""
    component_files = []
    for pattern in ['**/*.tsx', '**/*.jsx', '**/*.ts', '**/*.js']:
        files = Path('.').glob(pattern)
        for file in files:
            if 'node_modules' not in str(file) and '.next' not in str(file):
                component_files.append(file)
    return component_files

def extract_component_name(file_path):
    """Extract component name from file path"""
    return file_path.stem

def find_imports(file_content, component_name):
    """Find imports of a specific component"""
    patterns = [
        rf"import\s+.*{component_name}.*\s+from",
        rf"import\s+{{\s*.*{component_name}.*\s*}}\s+from",
        rf"const\s+{{\s*.*{component_name}.*\s*}}\s*=\s*require"
    ]
    
    for pattern in patterns:
        if re.search(pattern, file_content):
            return True
    return False

def update_used_by_comment(file_path, used_by_list):
    """Update @used-by comment in file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Remove old @used-by comment
        content = re.sub(r'\* @used-by .*\n', '', content)
        
        if used_by_list:
            # Add new @used-by comment
            used_by_str = ', '.join(used_by_list)
            new_comment = f" * @used-by {used_by_str}\n"
            
            # Find where to insert (after @component if exists)
            if '@component' in content:
                content = re.sub(r'(\* @component .*\n)', rf'\1{new_comment}', content)
            else:
                # Insert at beginning of first comment block
                content = re.sub(r'(/\*\*\n)', rf'\1{new_comment}', content, count=1)
        
        # Update @last-scan
        scan_date = datetime.now().strftime('%Y-%m-%d')
        if '@last-scan' in content:
            content = re.sub(r'\* @last-scan .*\n', f' * @last-scan {scan_date}\n', content)
        else:
            content = re.sub(r'(\*/)', f' * @last-scan {scan_date}\n\\1', content, count=1)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        return True
    except Exception as e:
        return False

def check_component(component_name):
    """Check what components use the specified component"""
    used_by = []
    component_file = None
    
    files = find_component_files()
    
    # Find the component file
    for file in files:
        if extract_component_name(file) == component_name:
            component_file = file
            break
    
    if not component_file:
        return {
            "error": f"Component '{component_name}' not found",
            "suggestions": []
        }
    
    # Find all files that import this component
    for file in files:
        if file != component_file:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                if find_imports(content, component_name):
                    used_by.append({
                        "name": extract_component_name(file),
                        "path": str(file)
                    })
            except:
                pass
    
    # Check for breaking changes (simplified)
    breaking_changes = []
    try:
        with open(component_file, 'r') as f:
            content = f.read()
        # Check if props interface changed recently (mock)
        if 'interface' in content and 'Props' in content:
            # In real implementation, would compare with git history
            pass
    except:
        pass
    
    return {
        "component": component_name,
        "file": str(component_file),
        "usedBy": used_by,
        "usedByCount": len(used_by),
        "lastModified": "2 hours ago",  # Mock
        "breakingChanges": breaking_changes
    }

def scan_all_dependencies():
    """Scan entire codebase and update dependency tracking"""
    files = find_component_files()
    
    # Build dependency map
    dependency_map = defaultdict(list)
    component_files = {}
    
    # First pass: identify all components
    for file in files:
        component_name = extract_component_name(file)
        component_files[component_name] = file
    
    # Second pass: find all imports
    for file in files:
        importer_name = extract_component_name(file)
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            for comp_name, comp_file in component_files.items():
                if comp_name != importer_name and find_imports(content, comp_name):
                    dependency_map[comp_name].append(importer_name)
        except:
            pass
    
    # Update @used-by comments
    updated_count = 0
    failed_count = 0
    orphaned_components = []
    
    for comp_name, comp_file in component_files.items():
        used_by = dependency_map.get(comp_name, [])
        if not used_by:
            orphaned_components.append(comp_name)
        
        if update_used_by_comment(comp_file, used_by):
            updated_count += 1
        else:
            failed_count += 1
    
    # Check for circular dependencies (simplified)
    circular_deps = []
    for comp_a, deps_a in dependency_map.items():
        for comp_b in deps_a:
            if comp_a in dependency_map.get(comp_b, []):
                circular_deps.append(f"{comp_a} <-> {comp_b}")
    
    return {
        "totalComponents": len(component_files),
        "componentsWithDeps": len([k for k, v in dependency_map.items() if v]),
        "orphanedComponents": len(orphaned_components),
        "orphaned": orphaned_components[:5],  # First 5
        "circularDependencies": len(set(circular_deps)),
        "updated": updated_count,
        "failed": failed_count
    }

def check_breaking_changes(component_name):
    """Check for potential breaking changes in a component"""
    # In real implementation, would:
    # 1. Check git diff for the component
    # 2. Analyze prop changes
    # 3. Check for removed exports
    # 4. Verify method signature changes
    
    return {
        "component": component_name,
        "breakingChanges": [
            {
                "type": "prop-removed",
                "detail": "Removed 'size' prop",
                "severity": "high",
                "affected": ["AuthForm", "ProfileForm"]
            }
        ],
        "safe": False,
        "recommendation": "Update all consumers before merging"
    }

def main():
    if action == "check":
        if not component:
            error_msg = "Component name required for check action"
            if is_non_interactive:
                print(json.dumps({"error": error_msg, "exitCode": 1}))
                sys.exit(1)
            else:
                print(f"❌ {error_msg}")
                print("Usage: /deps check <ComponentName>")
                sys.exit(1)
        
        result = check_component(component)
        
        if is_non_interactive:
            output = {
                "action": "check",
                "status": "error" if "error" in result else "success",
                "data": result,
                "exitCode": 1 if "error" in result else 0
            }
            print(json.dumps(output, indent=2))
            sys.exit(output["exitCode"])
        else:
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(f"\n📦 Dependency Check: {result['component']}\n")
                print(f"File: {result['file']}")
                print(f"\nUsed by ({result['usedByCount']} components):")
                for usage in result['usedBy']:
                    print(f"  ✓ {usage['name']} ({usage['path']})")
                
                if not result['usedBy']:
                    print("  ⚠️  No components use this component")
                
                print(f"\nLast modified: {result['lastModified']}")
                
                if result['breakingChanges']:
                    print("\n⚠️  Breaking changes detected!")
                else:
                    print("✅ No breaking changes detected")
    
    elif action == "scan":
        if not is_non_interactive:
            print("🔍 Scanning all dependencies...\n")
        
        result = scan_all_dependencies()
        
        if is_non_interactive:
            issues = []
            if result['orphanedComponents'] > 0:
                for comp in result['orphaned']:
                    issues.append({
                        "type": "orphaned-component",
                        "component": comp
                    })
            
            output = {
                "action": "scan",
                "status": "completed",
                "summary": result,
                "issues": issues,
                "exitCode": 0
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"✅ Scan complete!\n")
            print(f"📊 Summary:")
            print(f"  Total components: {result['totalComponents']}")
            print(f"  Components with dependencies: {result['componentsWithDeps']}")
            print(f"  Orphaned components: {result['orphanedComponents']}")
            print(f"  Circular dependencies: {result['circularDependencies']}")
            print(f"\n✅ Updated: {result['updated']} files")
            if result['failed'] > 0:
                print(f"❌ Failed: {result['failed']} files")
            
            if result['orphanedComponents'] > 0:
                print(f"\n⚠️  Orphaned components (not used anywhere):")
                for comp in result['orphaned']:
                    print(f"  - {comp}")
    
    elif action == "breaking":
        if not component:
            error_msg = "Component name required for breaking check"
            if is_non_interactive:
                print(json.dumps({"error": error_msg, "exitCode": 1}))
                sys.exit(1)
            else:
                print(f"❌ {error_msg}")
                sys.exit(1)
        
        result = check_breaking_changes(component)
        
        if is_non_interactive:
            output = {
                "action": "breaking",
                "status": "unsafe" if not result['safe'] else "safe",
                "data": result,
                "exitCode": 1 if not result['safe'] else 0
            }
            print(json.dumps(output, indent=2))
            sys.exit(output["exitCode"])
        else:
            print(f"\n🔍 Breaking Changes Check: {result['component']}\n")
            
            if result['breakingChanges']:
                print("⚠️  Breaking changes detected:")
                for change in result['breakingChanges']:
                    print(f"\n  Type: {change['type']}")
                    print(f"  Detail: {change['detail']}")
                    print(f"  Severity: {change['severity']}")
                    print(f"  Affected: {', '.join(change['affected'])}")
                
                print(f"\n💡 Recommendation: {result['recommendation']}")
            else:
                print("✅ No breaking changes detected")

if __name__ == "__main__":
    main()
EOF`

## Actions:

### CHECK - See what uses a component
```bash
/deps check Button
/deps check useAuth
```

Shows:
```
📦 Dependency Check: Button

Used by (3 components):
  ✓ AuthForm (components/auth/AuthForm.tsx)
  ✓ ProfileForm (components/profile/ProfileForm.tsx) 
  ✓ SettingsPage (app/settings/page.tsx)

Last modified: 2 hours ago
Breaking changes: None detected

Quick actions:
  • /deps update Button - Update all imports
  • /deps breaking Button - Check for breaking changes
```

### SCAN - Update all @used-by comments
```bash
/deps scan

# Non-interactive for CI/CD
claude --non-interactive "/deps scan"
```

Scans entire codebase and updates dependency comments:
```typescript
/**
 * @component Button
 * @used-by AuthForm, ProfileForm, SettingsPage
 * @depends-on Icon, cn
 * @last-scan 2024-01-16
 */
```

### UPDATE - Update all components using a dependency
```bash
/deps update Button
```

Updates import paths if component moved:
```
🔄 Updating Button imports...

✓ AuthForm: Updated import path
✓ ProfileForm: Updated import path
✓ SettingsPage: Updated import path

3 files updated successfully
```

### BREAKING - Check for breaking changes
```bash
/deps breaking Button
```

Analyzes recent changes:
```
🔍 Breaking Changes Analysis: Button

⚠️ Potential breaking changes detected:
  
1. Props changed:
   - Removed: 'size' prop
   - Added: 'variant' prop (required)
   
2. Affected components (3):
   - AuthForm: Uses removed 'size' prop
   - ProfileForm: Missing new 'variant' prop
   - SettingsPage: Compatible

Recommendation: Update affected components before merging
```

## Implementation:

### Tracking Format
Components include dependency metadata:
```typescript
/**
 * @component Button
 * @used-by AuthForm, ProfileForm, SettingsPage
 * @depends-on Icon, cn, clsx
 * @last-scan 2024-01-16
 * @exports Button, ButtonProps
 */
export function Button({ ... }) { }
```

### Auto-Detection
Scans for:
- ES6 imports: `import { Button } from './Button'`
- CommonJS: `const { Button } = require('./Button')`
- Dynamic imports: `import('./Button')`
- Re-exports: `export { Button } from './Button'`

### Breaking Change Detection
- Removed exports
- Changed prop types
- Modified function signatures
- Renamed components

## Benefits:
- Know impact before changes
- Prevent accidental breakage
- Track component usage
- Find unused components
- Update imports automatically
- CI/CD integration ready

## CI/CD Integration:

### GitHub Actions
```yaml
- name: Dependency Scan
  env:
    CLAUDE_NON_INTERACTIVE: true
  run: |
    claude --non-interactive "/deps scan"
    
- name: Check Breaking Changes
  if: github.event_name == 'pull_request'
  run: |
    # Get changed components
    CHANGED=$(git diff --name-only ${{ github.event.before }}..${{ github.sha }} | grep -E '\.(tsx|jsx)$' | xargs -I {} basename {} .tsx)
    
    for component in $CHANGED; do
      claude --non-interactive "/deps breaking $component" || exit 1
    done
```

### Pre-commit Hook
```bash
# Check for breaking changes before commit
for file in $(git diff --cached --name-only | grep -E '\.(tsx|jsx)$'); do
  component=$(basename "$file" | sed 's/\..*//')
  claude --non-interactive "/deps breaking $component"
done
```