# Stage Validate Command

Validate completion of PRD phases with automated gates before proceeding to next stage.

## Arguments:
- $ACTION: check|require|override|status
- $STAGE: 1|2|3|current|all

## Purpose:
Ensures each development phase meets exit criteria before moving forward, preventing incomplete implementations and technical debt.

## Non-Interactive Mode Support

When running in non-interactive mode (CI/CD), outputs structured JSON and returns appropriate exit codes:

```bash
# In CI/CD pipeline
claude --non-interactive "/stage-validate check 1"

# Returns JSON output:
{
  "stage": 1,
  "status": "incomplete",
  "progress": 75,
  "passed": 6,
  "failed": 2,
  "total": 8,
  "failures": [
    "session-management",
    "testing-framework"
  ],
  "exitCode": 1
}
```

## Enhanced Implementation with Non-Interactive Support

!`python3 << 'EOF'
import json
import os
import sys
from datetime import datetime

# Check if running in non-interactive mode
is_non_interactive = os.environ.get('CLAUDE_NON_INTERACTIVE', 'false').lower() == 'true'

action = """$ACTION""".strip() or "check"
stage = """$STAGE""".strip() or "current"

# Validation criteria for each stage
stage_criteria = {
    1: {
        "name": "Foundation",
        "criteria": {
            "Database Schema": [
                ("Models defined", lambda: check_files_exist("lib/db/schema/*.ts"), "Create database models"),
                ("Migrations created", lambda: check_files_exist("migrations/*.sql"), "Run: drizzle-kit generate"),
                ("Test data seeded", lambda: check_files_exist("scripts/seed.ts"), "Create seed script"),
            ],
            "API Structure": [
                ("Routes configured", lambda: check_files_exist("app/api/**/*.ts"), "Create API routes"),
                ("Middleware setup", lambda: check_file_exists("middleware.ts"), "Setup middleware"),
                ("Error handling", lambda: check_pattern_in_files("app/api", "try.*catch"), "Add error handling"),
            ],
            "Authentication": [
                ("Basic auth working", lambda: check_files_exist("lib/auth/*.ts"), "Implement auth"),
                ("Session management", lambda: check_pattern_in_files("lib/auth", "session"), "Add sessions"),
                ("Password reset", lambda: check_files_exist("app/api/auth/reset/*.ts"), "Add password reset"),
            ],
            "Testing Setup": [
                ("Unit test framework", lambda: check_file_exists("vitest.config.ts"), "Run: /test-runner init"),
                ("E2E configured", lambda: check_file_exists("playwright.config.ts"), "Setup Playwright"),
            ]
        }
    },
    2: {
        "name": "Core Features",
        "criteria": {
            "Features": [
                ("All PRD features", lambda: True, "Implement remaining features"),  # Would check task status
                ("Error states", lambda: check_pattern_in_files("components", "error"), "Add error handling"),
                ("Loading states", lambda: check_pattern_in_files("components", "loading"), "Add loading states"),
            ],
            "UI": [
                ("Components render", lambda: True, "Fix rendering issues"),
                ("Forms validate", lambda: check_pattern_in_files("components", "useForm"), "Add validation"),
                ("Mobile responsive", lambda: check_pattern_in_files("components", "md:|lg:"), "Add responsive styles"),
            ]
        }
    },
    3: {
        "name": "Polish",
        "criteria": {
            "Performance": [
                ("Bundle optimized", lambda: True, "Run: npm run analyze"),
                ("Images optimized", lambda: check_files_exist("public/**/*.webp"), "Optimize images"),
            ],
            "Security": [
                ("Auth tested", lambda: check_files_exist("tests/auth/*.test.ts"), "Add auth tests"),
                ("Rate limiting", lambda: check_pattern_in_files("middleware", "rateLimit"), "Add rate limiting"),
            ]
        }
    }
}

def check_files_exist(pattern):
    """Mock function - would check if files matching pattern exist"""
    import random
    return random.choice([True, False])

def check_file_exists(filepath):
    """Mock function - would check if specific file exists"""
    import random
    return random.choice([True, False])

def check_pattern_in_files(directory, pattern):
    """Mock function - would grep for pattern in directory"""
    import random
    return random.choice([True, False])

def validate_stage(stage_num):
    """Validate a specific stage and return results"""
    if stage_num not in stage_criteria:
        return {"error": f"Invalid stage: {stage_num}"}
    
    stage_info = stage_criteria[stage_num]
    results = {
        "stage": stage_num,
        "name": stage_info["name"],
        "categories": {},
        "total": 0,
        "passed": 0,
        "failed": 0,
        "failures": []
    }
    
    for category, checks in stage_info["criteria"].items():
        category_results = []
        for check_name, check_func, fix_hint in checks:
            passed = check_func()
            category_results.append({
                "check": check_name,
                "passed": passed,
                "fix": fix_hint if not passed else None
            })
            results["total"] += 1
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["failures"].append(f"{category}/{check_name}")
        
        results["categories"][category] = category_results
    
    results["progress"] = int((results["passed"] / results["total"]) * 100)
    results["status"] = "complete" if results["failed"] == 0 else "incomplete"
    
    return results

def format_interactive_output(results):
    """Format results for interactive display"""
    print(f"\n=== VALIDATING STAGE {results['stage']}: {results['name']} ===\n")
    
    for category, checks in results["categories"].items():
        all_passed = all(check["passed"] for check in checks)
        icon = "✅" if all_passed else "⚠️" if any(check["passed"] for check in checks) else "❌"
        
        print(f"{icon} {category}")
        for check in checks:
            if check["passed"]:
                print(f"   ✓ {check['check']}")
            else:
                print(f"   ✗ {check['check']}")
                if check["fix"]:
                    print(f"     → {check['fix']}")
        print()
    
    print(f"STAGE {results['stage']} STATUS: {results['progress']}% Complete")
    
    if results["status"] == "incomplete":
        print(f"❌ Cannot proceed to Stage {results['stage'] + 1}")
        print(f"\nMissing items:")
        for i, failure in enumerate(results["failures"], 1):
            print(f"{i}. {failure.replace('/', ': ')}")
    else:
        print(f"✅ Stage {results['stage']} complete! Ready for Stage {results['stage'] + 1}")

def main():
    if action == "check":
        # Determine which stage to check
        stage_num = 1 if stage == "current" else int(stage) if stage.isdigit() else 1
        
        # Validate the stage
        results = validate_stage(stage_num)
        
        if is_non_interactive:
            # Non-interactive mode: output JSON and exit
            output = {
                **results,
                "timestamp": datetime.now().isoformat(),
                "exitCode": 0 if results["status"] == "complete" else 1
            }
            print(json.dumps(output, indent=2))
            sys.exit(output["exitCode"])
        else:
            # Interactive mode: pretty print
            format_interactive_output(results)
            
    elif action == "status":
        # Show status of all stages
        all_results = []
        for stage_num in [1, 2, 3]:
            results = validate_stage(stage_num)
            all_results.append(results)
        
        if is_non_interactive:
            output = {
                "stages": all_results,
                "overall_progress": sum(r["progress"] for r in all_results) // len(all_results),
                "current_stage": next((r["stage"] for r in all_results if r["status"] == "incomplete"), 4),
                "exitCode": 0
            }
            print(json.dumps(output, indent=2))
            sys.exit(0)
        else:
            print("\n=== PROJECT STAGE STATUS ===\n")
            for results in all_results:
                status_icon = "✅" if results["status"] == "complete" else "⚠️" if results["progress"] > 0 else "🔒"
                print(f"Stage {results['stage']}: {results['name']} {status_icon} {results['progress']}%")
            
            overall = sum(r["progress"] for r in all_results) // len(all_results)
            print(f"\n📊 Overall Progress: {overall}% Complete")

if __name__ == "__main__":
    main()
EOF`

## Actions:

### CHECK - Validate current stage
```bash
/stage-validate check 1
/stage-validate check current

# Non-interactive mode for CI/CD
claude --non-interactive "/stage-validate check 1"
```

Runs automated checks:
```
=== VALIDATING STAGE 1: Foundation ===

✅ Database Schema
   - All models defined
   - Migrations created
   - Test data seeded

✅ API Structure  
   - Routes configured
   - Middleware setup
   - Error handling

⚠️ Authentication
   - Basic auth working
   - [ ] Session management incomplete
   - [ ] Password reset missing

❌ Testing Setup
   - [ ] Unit test framework missing
   - [ ] E2E not configured

STAGE 1 STATUS: 75% Complete
❌ Cannot proceed to Stage 2

Missing items:
1. Complete session management
2. Add password reset flow
3. Setup testing framework

Run: /stage-validate require 1
```

### REQUIRE - Enforce validation
```bash
/stage-validate require 2
```

This:
1. Blocks proceeding until criteria met
2. Updates task list with missing items
3. Sets focused context profile
4. Shows exact commands to run

### STATUS - Overview of all stages
```bash
/stage-validate status

# Non-interactive mode
claude --non-interactive "/stage-validate status"
```

Output:
```
=== PROJECT STAGE STATUS ===

Stage 1: Foundation ✅ COMPLETE
  Duration: 2 days
  Commits: 23
  Tests: 45 passing

Stage 2: Core Features ⚠️ IN PROGRESS (82%)
  Started: Today 9:00 AM
  Remaining: 3 tasks
  Estimate: 2 hours

Stage 3: Polish 🔒 LOCKED
  Unlocks: After Stage 2
  Estimated: 1 day

📊 Overall Progress: 54% Complete
```

### OVERRIDE - Skip validation (with reason)
```bash
/stage-validate override 1 --reason "Client demo, auth incomplete"
```

Records override in project log

## Exit Criteria Configuration:

Each PRD automatically generates stage validations:

```typescript
interface StageValidation {
  stage: number;
  name: string;
  criteria: {
    category: string;
    items: ValidationItem[];
  }[];
  automated: AutomatedCheck[];
  manual: ManualCheck[];
}

interface ValidationItem {
  description: string;
  validator: () => boolean;
  errorMessage: string;
  fixCommand?: string;
}
```

## Stage 1: Foundation Criteria
```yaml
Database:
  - Schema fully defined
  - Migrations run successfully
  - Indexes created
  - Test data available

API:
  - All routes return 200/404
  - Error handling middleware
  - Request validation
  - CORS configured

Auth:
  - User registration works
  - Login returns token
  - Protected routes secured
  - Session management

Environment:
  - All env vars documented
  - Dev/prod configs separate
  - Secrets not in code
```

## Stage 2: Core Features Criteria  
```yaml
Features:
  - All PRD features implemented
  - Happy path tested
  - Error states handled
  - Loading states added

UI:
  - All components render
  - Forms validate properly  
  - Responsive on mobile
  - Accessibility basics

Integration:
  - Frontend connects to API
  - Real data displayed
  - CRUD operations work
  - File uploads functional
```

## Stage 3: Polish Criteria
```yaml
Performance:
  - Lighthouse score > 90
  - Bundle size optimized
  - Images optimized
  - API responses < 200ms

Security:
  - Auth fully tested
  - OWASP checklist passed
  - Rate limiting active
  - Input sanitization

Production:
  - Error tracking setup
  - Analytics configured
  - Monitoring active
  - Deployment automated
```

## Automated Validators:

### Code Validators
```bash
# Run automatically during validation
npm run typecheck      # No TypeScript errors
npm run lint          # No linting errors  
npm run test          # All tests pass
npm run build         # Build succeeds
```

### Design System Validators
```bash
/vd --strict          # Full design validation
```

### Security Validators
```bash
/security-check --stage 1
```

### Custom Validators
Each stage can have custom validation scripts:
```
.claude/validators/
  ├── stage-1-foundation.js
  ├── stage-2-features.js
  └── stage-3-polish.js
```

## Integration with Workflow:

### 1. PRD Auto-generates Validators
When creating PRD, validators are created:
```markdown
## Stage 1 Exit Criteria
- [ ] All database models defined
- [ ] API endpoints return correct status
- [ ] Authentication flow complete
- [ ] Automated tests: /stage-validate check 1
```

### 2. Task Integration
Tasks automatically tagged with stage:
```
[Stage 1] Create user model
[Stage 1] Setup auth routes
[Stage 2] Build dashboard component
```

### 3. Git Branch Protection
```bash
# Attempts to merge stage-2 work before stage-1 complete
❌ Stage validation failed
   Stage 1 incomplete (85%)
   Run: /stage-validate status
```

### 4. Checkpoint Integration
Checkpoints include stage status:
```json
{
  "checkpoint": "auth-work-tuesday",
  "stage": {
    "current": 1,
    "progress": 85,
    "blockers": ["session-management", "test-setup"]
  }
}
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Stage Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code
        
      - name: Validate Current Stage
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --non-interactive "/stage-validate check current" || exit 1
          
      - name: Check Overall Progress
        run: |
          claude --non-interactive "/stage-validate status"
```

### GitLab CI Example
```yaml
stage-validation:
  stage: test
  script:
    - npm install -g @anthropic-ai/claude-code
    - claude --non-interactive "/stage-validate check current"
  only:
    - merge_requests
```

## Smart Features:

### Auto-Fix Suggestions
```
❌ Validation Failed: No test framework

Suggested fix:
/test-runner init --framework vitest
```

### Rollback Protection
```
⚠️ Detected work from Stage 2
   But Stage 1 only 85% complete
   
Options:
1. Complete Stage 1 first
2. Move Stage 2 work to branch
3. Override (not recommended)
```

### Time Tracking
```
📊 Stage Metrics:
   Stage 1: 2.5 days (est: 2 days)
   Stage 2: In progress
   
   Velocity: 92% of estimate
```

## Benefits:
- Prevents incomplete features
- Enforces quality gates
- Clear progress visibility
- Reduces technical debt
- Improves handoffs
- Client-ready milestones
- CI/CD automation support