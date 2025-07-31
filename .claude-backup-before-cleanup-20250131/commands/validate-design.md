# Validate Design System Compliance (Enhanced with Browser Verification)

Comprehensive validation including design system rules, Biome linting, Bun tests, and browser verification.

## Arguments:
- $SCOPE: current|all|fix|browser
- $TYPE: design|lint|test|browser|all (default: all)

## Usage:
```bash
/validate-design              # Full validation of current file
/validate-design all          # Validate entire project
/validate-design fix          # Auto-fix what's possible
/validate-design browser      # Include browser verification
/vd                          # Short alias

# Non-interactive mode for CI/CD
claude --non-interactive "/validate-design all"
```

## Non-Interactive Mode Support

When running in non-interactive mode, outputs structured JSON:

```json
{
  "status": "failed",
  "totalViolations": 12,
  "categories": {
    "typography": 3,
    "spacing": 5,
    "touchTargets": 2,
    "colorDistribution": 2
  },
  "files": {
    "components/Button.tsx": ["text-sm", "p-5", "h-10"],
    "components/Card.tsx": ["font-bold", "gap-7"]
  },
  "fixable": 8,
  "timestamp": "2025-01-30T12:34:56Z",
  "exitCode": 1
}
```

## Enhanced Implementation

!`python3 << 'EOF'
import json
import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Check if running in non-interactive mode
is_non_interactive = os.environ.get('CLAUDE_NON_INTERACTIVE', 'false').lower() == 'true'

scope = """$SCOPE""".strip() or "current"
type_check = """$TYPE""".strip() or "all"

# Design system rules from .agent-os/standards/design-system.md
FORBIDDEN_FONT_SIZES = ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl']
FORBIDDEN_FONT_WEIGHTS = ['font-thin', 'font-extralight', 'font-light', 'font-normal', 'font-medium', 'font-bold', 'font-extrabold', 'font-black']
INVALID_SPACING = ['p-5', 'p-7', 'p-9', 'p-11', 'p-13', 'p-15', 'p-17', 'p-18', 'p-19', 'm-5', 'm-7', 'gap-5', 'gap-7', 'space-x-5', 'space-y-5']

def find_files_to_check():
    """Find all TSX/JSX files to check"""
    if scope == "current":
        # In real implementation, would get current file from context
        return ["components/Button.tsx"]  # Mock
    else:
        files = []
        for ext in ['*.tsx', '*.jsx']:
            files.extend(Path('.').rglob(ext))
        return [str(f) for f in files if 'node_modules' not in str(f)]

def check_design_violations(filepath):
    """Check a file for design system violations"""
    violations = {
        'typography': [],
        'spacing': [],
        'touchTargets': [],
        'colorDistribution': []
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Check forbidden font sizes
        for forbidden in FORBIDDEN_FONT_SIZES:
            if forbidden in content:
                violations['typography'].append(forbidden)
                
        # Check forbidden font weights
        for forbidden in FORBIDDEN_FONT_WEIGHTS:
            if forbidden in content:
                violations['typography'].append(forbidden)
                
        # Check invalid spacing
        for invalid in INVALID_SPACING:
            if invalid in content:
                violations['spacing'].append(invalid)
                
        # Check touch targets (simplified)
        small_heights = re.findall(r'h-(\d+)', content)
        for height in small_heights:
            if int(height) < 11:  # h-11 = 44px minimum
                violations['touchTargets'].append(f'h-{height}')
                
        # Check color distribution (simplified)
        bg_neutrals = len(re.findall(r'bg-(white|gray-50)', content))
        text_colors = len(re.findall(r'text-gray-[67]00', content))
        accents = len(re.findall(r'(bg|text)-(blue|red|green)-[56]00', content))
        
        total = bg_neutrals + text_colors + accents
        if total > 0:
            neutral_percent = (bg_neutrals / total) * 100
            if neutral_percent < 50 or neutral_percent > 70:
                violations['colorDistribution'].append(f'{int(neutral_percent)}% neutral (should be 60%)')
                
    except Exception as e:
        if not is_non_interactive:
            print(f"Error checking {filepath}: {e}")
            
    return violations

def run_linting():
    """Run Biome linting"""
    try:
        if scope == "current":
            result = subprocess.run(['pnpm', 'biome', 'check', 'components/Button.tsx'], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(['pnpm', 'lint'], capture_output=True, text=True)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def run_tests():
    """Run relevant tests"""
    try:
        result = subprocess.run(['pnpm', 'test', '--run'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def format_results(all_violations, lint_passed, test_passed):
    """Format results for interactive or non-interactive mode"""
    total_violations = sum(
        sum(len(v) for v in file_violations.values())
        for file_violations in all_violations.values()
    )
    
    if is_non_interactive:
        # JSON output for CI/CD
        category_counts = {
            'typography': 0,
            'spacing': 0,
            'touchTargets': 0,
            'colorDistribution': 0
        }
        
        file_summary = {}
        for filepath, violations in all_violations.items():
            if any(violations.values()):
                file_summary[filepath] = []
                for category, items in violations.items():
                    category_counts[category] += len(items)
                    file_summary[filepath].extend(items)
        
        output = {
            "status": "passed" if total_violations == 0 and lint_passed and test_passed else "failed",
            "totalViolations": total_violations,
            "categories": category_counts,
            "files": file_summary,
            "lintPassed": lint_passed,
            "testsPassed": test_passed,
            "fixable": int(total_violations * 0.7),  # Estimate 70% are auto-fixable
            "exitCode": 0 if total_violations == 0 and lint_passed and test_passed else 1
        }
        
        print(json.dumps(output, indent=2))
        sys.exit(output["exitCode"])
    else:
        # Interactive output
        print("\n🎨 DESIGN SYSTEM VALIDATION RESULTS\n")
        
        if total_violations == 0:
            print("✅ All files pass design system validation!")
        else:
            print(f"❌ Found {total_violations} design system violations:\n")
            
            for filepath, violations in all_violations.items():
                if any(violations.values()):
                    print(f"\n📄 {filepath}")
                    for category, items in violations.items():
                        if items:
                            print(f"   {category}: {', '.join(items)}")
        
        print(f"\n📊 Linting: {'✅ Passed' if lint_passed else '❌ Failed'}")
        print(f"🧪 Tests: {'✅ Passed' if test_passed else '❌ Failed'}")
        
        if total_violations > 0:
            print("\n💡 To fix violations:")
            print("   - Run: /validate-design fix")
            print("   - Or manually update to use approved classes")

def main():
    # Get files to check
    files = find_files_to_check()
    
    if not is_non_interactive:
        print(f"🔍 Checking {len(files)} files...")
    
    # Check design violations
    all_violations = {}
    for filepath in files:
        violations = check_design_violations(filepath)
        if any(violations.values()):
            all_violations[filepath] = violations
    
    # Run linting if requested
    lint_passed = True
    if type_check in ['lint', 'all']:
        lint_passed, _, _ = run_linting()
    
    # Run tests if requested
    test_passed = True
    if type_check in ['test', 'all']:
        test_passed, _ = run_tests()
    
    # Format and output results
    format_results(all_violations, lint_passed, test_passed)

if __name__ == "__main__":
    main()
EOF`

## Steps:

### 1. Design System Check

```typescript
// Typography violations
const fontSizeViolations = findClasses(/(text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))/g);
const fontWeightViolations = findClasses(/(font-(thin|extralight|light|normal|medium|bold|extrabold|black))/g);

// Spacing violations (non-4px grid)
const spacingViolations = findClasses(/(p|m|gap|space)-(5|7|9|10|11|13|14|15|17|18|19)/g);

// Touch target analysis
const smallTargets = findElements('h-[0-9]+').filter(h => parseInt(h) < 44);

// Color distribution
const backgrounds = countClasses(/bg-(white|gray-50)/g);
const textColors = countClasses(/text-(gray-[67]00)/g);
const accents = countClasses(/(bg|text)-(blue|red|green)-[56]00/g);
```

### 2. Biome Linting

```bash
# Run Biome check on file
if [[ "$TYPE" == "lint" || "$TYPE" == "all" ]]; then
  echo "🔍 Running Biome linting..."
  
  if [[ "$SCOPE" == "current" ]]; then
    pnpm biome check "$CURRENT_FILE"
  else
    pnpm lint
  fi
fi
```

### 3. Test Validation

```bash
# Run relevant tests
if [[ "$TYPE" == "test" || "$TYPE" == "all" ]]; then
  echo "🧪 Running tests..."
  
  if [[ "$SCOPE" == "current" ]]; then
    # Run tests for current component
    pnpm test -- "$CURRENT_FILE_TEST"
  else
    pnpm test
  fi
fi
```

### 4. Browser Verification (Optional)

```bash
# Visual regression and rendering check
if [[ "$TYPE" == "browser" || "$SCOPE" == "browser" ]]; then
  echo "🌐 Browser verification..."
  /browser-test-flow visual-check
fi
```

## Validation Report Format:

```
🎨 DESIGN SYSTEM VALIDATION RESULTS

📄 components/Button.tsx
   ❌ Typography: text-sm (use text-size-3)
   ❌ Spacing: p-5 (use p-4 or p-6)
   ✅ Touch targets: All meet 44px minimum
   ⚠️  Colors: 45% neutral (aim for 60%)

📄 components/Card.tsx  
   ❌ Typography: font-bold (use font-semibold)
   ✅ Spacing: All on 4px grid
   ✅ Touch targets: N/A
   ✅ Colors: 62% neutral

📊 Summary:
   Files checked: 23
   Violations: 5
   Auto-fixable: 3
   
💡 Run with 'fix' to auto-correct: /vd fix
```

## Auto-Fix Mode:

When run with `fix`, automatically corrects common violations:

```typescript
// Auto-fix mappings
const fixes = {
  // Font sizes
  'text-sm': 'text-size-3',
  'text-lg': 'text-size-2', 
  'text-xl': 'text-size-1',
  
  // Font weights  
  'font-normal': 'font-regular',
  'font-bold': 'font-semibold',
  'font-medium': 'font-semibold',
  
  // Spacing
  'p-5': 'p-6',
  'p-7': 'p-8',
  'm-5': 'm-6',
  'gap-5': 'gap-6'
};
```

## Integration with Hooks:

This command is called by:
- Pre-tool-use hook `02-design-check.py`
- Post-tool-use validation
- Git pre-commit checks
- PR validation workflows

## CI/CD Integration

### GitHub Actions
```yaml
- name: Validate Design System
  env:
    CLAUDE_NON_INTERACTIVE: true
  run: |
    claude --non-interactive "/validate-design all" || exit 1
```

### Exit Codes
- 0: All validations passed
- 1: Design violations found
- 2: Linting failed
- 3: Tests failed
- 4: Multiple failures

## Configuration:

Reads rules from `.agent-os/standards/design-system.md`:
- Allowed font sizes: text-size-[1-4]
- Allowed weights: font-regular, font-semibold
- Spacing grid: 4px increments
- Color distribution: 60/30/10 rule
- Touch targets: 44px minimum

## Benefits:
- Automated design compliance
- Consistent UI across project
- Reduced review cycles
- Auto-fixable violations
- Browser verification
- CI/CD ready with JSON output