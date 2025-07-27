# Technical Implementation Guide: Priority 1 Features

## 1. Snapshot & Rollback System

### Architecture Overview

```
.claude/snapshots/
├── manifest.json                    # Global snapshot registry
├── 2025-01-15-14-30-00-auth/      # Timestamp + description
│   ├── manifest.json               # Snapshot metadata
│   ├── files/                      # Changed files
│   │   ├── components/
│   │   │   └── auth/
│   │   │       └── LoginForm.tsx
│   │   └── lib/
│   │       └── auth.ts
│   ├── git-status.json            # Git state at snapshot time
│   └── context.json               # Claude context state
└── .gitignore                     # Ignore snapshots in git
```

### Implementation Details

#### Pre-Tool-Use Hook: `00a-snapshot-manager.py`

```python
#!/usr/bin/env python3
"""
Automatic snapshot creation before risky operations
"""

import json
import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

class SnapshotManager:
    def __init__(self):
        self.snapshot_dir = Path('.claude/snapshots')
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.snapshot_dir / 'manifest.json'
        self.load_manifest()
        
    def should_snapshot(self, tool_name, tool_input):
        """Determine if operation needs snapshot"""
        
        # Always snapshot for these tools
        if tool_name in ['MultiEdit', 'Bash']:
            return True
            
        # Check for risky operations
        if tool_name in ['Write', 'Edit']:
            file_path = tool_input.get('file_path', '')
            
            # Critical files
            if any(critical in file_path for critical in [
                'package.json', '.env', 'tsconfig.json', 
                'next.config.js', 'drizzle.config.ts'
            ]):
                return True
                
            # Check recent edit count
            recent_edits = self.get_recent_edits()
            if recent_edits > 5:
                return True
                
        return False
        
    def create_snapshot(self, description="auto"):
        """Create a new snapshot"""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        snapshot_name = f"{timestamp}-{description}"
        snapshot_path = self.snapshot_dir / snapshot_name
        
        # Create snapshot directory
        snapshot_path.mkdir(parents=True, exist_ok=True)
        
        # Get changed files from git
        changed_files = self.get_changed_files()
        
        # Copy changed files
        files_dir = snapshot_path / 'files'
        for file_path in changed_files:
            if Path(file_path).exists():
                dest = files_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest)
                
        # Save metadata
        metadata = {
            'timestamp': timestamp,
            'description': description,
            'files': changed_files,
            'file_count': len(changed_files),
            'git_branch': self.get_git_branch(),
            'git_commit': self.get_git_commit()
        }
        
        with open(snapshot_path / 'manifest.json', 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Update global manifest
        self.add_to_manifest(snapshot_name, metadata)
        
        # Cleanup old snapshots
        self.cleanup_old_snapshots()
        
        return snapshot_name
```

#### Command Implementation: `/snapshot`

```markdown
# Snapshot Command

Take a snapshot of current state or manage existing snapshots.

## Arguments:
- $ACTION: create|list|preview|rollback|diff|auto
- $SNAPSHOT_ID: Snapshot number or name (for preview/rollback/diff)
- $DESCRIPTION: Description for create action

## Actions:

### Create
```bash
/snapshot create "before auth refactor"
```
Creates manual snapshot with description.

### List
```bash
/snapshot list
```
Shows recent snapshots:
```
1. 2025-01-15-14:30:00-auth (2 hours ago, 5 files)
2. 2025-01-15-13:00:00-auto (3 hours ago, 12 files)
3. 2025-01-15-10:00:00-migration (6 hours ago, 3 files)
```

### Preview
```bash
/snapshot preview 1
```
Shows what would be restored:
```
Snapshot: 2025-01-15-14:30:00-auth
Files that would be restored:
- components/auth/LoginForm.tsx (modified)
- lib/auth.ts (modified)
- app/api/auth/route.ts (deleted - would be restored)
```

### Rollback
```bash
/snapshot rollback 1
```
Restores files from snapshot with confirmation:
```
⚠️  This will restore 5 files from snapshot 2025-01-15-14:30:00-auth
Current files will be backed up to .claude/snapshots/rollback-backup/
Continue? (y/n)
```

### Diff
```bash
/snapshot diff 1 2
```
Shows differences between two snapshots.

### Auto
```bash
/snapshot auto
```
Toggles automatic snapshot creation.

## Integration with existing systems:

1. **State Save Integration**
   - Snapshots include current context state
   - Can restore both files and Claude context

2. **Git Integration**
   - Tracks git branch/commit at snapshot time
   - Can show git diff alongside snapshot diff

3. **Hook System**
   - Pre-tool-use hook creates automatic snapshots
   - Post-rollback hook updates context
```

### Cleanup Policy

```python
def cleanup_old_snapshots(self, keep_count=20):
    """Remove old snapshots, keeping most recent"""
    snapshots = self.get_all_snapshots()
    
    if len(snapshots) > keep_count:
        # Sort by timestamp
        snapshots.sort(key=lambda x: x['timestamp'])
        
        # Remove oldest
        to_remove = snapshots[:-keep_count]
        for snapshot in to_remove:
            # Skip if marked as important
            if not snapshot.get('important', False):
                shutil.rmtree(self.snapshot_dir / snapshot['name'])
                
        self.update_manifest()
```

## 2. TypeScript Error Feedback Loop

### Architecture

```
Feedback Loop:
Claude writes code → Hook detects TS file → Run tsc → Parse errors → Feed back to Claude
                                                                            ↓
                                                                   Claude fixes errors
```

### Implementation: `07-typescript-validator.py`

```python
#!/usr/bin/env python3
"""
TypeScript validation hook - provides immediate error feedback
"""

import json
import subprocess
import sys
import re
from pathlib import Path

class TypeScriptValidator:
    def __init__(self):
        self.project_root = self.find_project_root()
        self.tsconfig_path = self.project_root / 'tsconfig.json'
        self.cache_file = Path('.claude/.tsc-cache.json')
        
    def should_validate(self, tool_name, file_path):
        """Check if we should run TypeScript validation"""
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            return False
            
        # Only for TS/TSX files
        return file_path.endswith(('.ts', '.tsx'))
        
    def run_incremental_check(self, changed_files):
        """Run TypeScript check with incremental compilation"""
        
        # Build file list for targeted checking
        file_args = []
        for file in changed_files:
            if file.endswith(('.ts', '.tsx')):
                file_args.append(file)
                
        if not file_args:
            return None
            
        # Run tsc with incremental flag
        cmd = [
            'npx', 'tsc',
            '--noEmit',
            '--incremental',
            '--tsBuildInfoFile', '.claude/.tsbuildinfo',
            '--pretty', 'false',
            '--skipLibCheck'
        ] + file_args
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode == 0:
            return None
            
        # Parse errors
        errors = self.parse_tsc_output(result.stdout)
        return self.format_error_feedback(errors)
        
    def parse_tsc_output(self, output):
        """Parse TypeScript compiler output"""
        errors = []
        
        # Pattern: file(line,col): error TS1234: message
        pattern = r'(.+?)\((\d+),(\d+)\): error (TS\d+): (.+)'
        
        for match in re.finditer(pattern, output):
            errors.append({
                'file': match.group(1),
                'line': int(match.group(2)),
                'column': int(match.group(3)),
                'code': match.group(4),
                'message': match.group(5)
            })
            
        return errors
        
    def format_error_feedback(self, errors):
        """Format errors for Claude"""
        if not errors:
            return None
            
        # Group by file
        by_file = {}
        for error in errors:
            file = error['file']
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(error)
            
        # Format message
        msg = "🚨 TypeScript Errors Detected\n\n"
        
        for file, file_errors in by_file.items():
            msg += f"📄 {file}:\n"
            for error in file_errors[:3]:  # Limit to 3 per file
                msg += f"  Line {error['line']}: {error['message']}\n"
            
            if len(file_errors) > 3:
                msg += f"  ... and {len(file_errors) - 3} more errors\n"
            msg += "\n"
            
        msg += "Fix these TypeScript errors before continuing.\n"
        msg += "Run 'npm run typecheck' to see all errors."
        
        return msg
        
    def get_fix_suggestions(self, error):
        """Provide fix suggestions for common errors"""
        suggestions = {
            'TS2304': "Import the missing type or declare it",
            'TS2339': "Check property exists or add type annotation",
            'TS2345': "Type mismatch - check argument types",
            'TS2741': "Missing required properties in object",
            'TS7006': "Add explicit type annotation"
        }
        
        return suggestions.get(error['code'], "Check TypeScript documentation")
```

### Integration with Main Hook System

```python
def main():
    """Main hook entry point"""
    try:
        # Read Claude's input
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_output = input_data.get('tool_output', {})
        
        # Only run after successful file operations
        if tool_output.get('status') != 'success':
            sys.exit(0)
            
        validator = TypeScriptValidator()
        
        # Check if we should validate
        file_path = tool_input.get('file_path', '')
        if not validator.should_validate(tool_name, file_path):
            sys.exit(0)
            
        # Get list of recently changed files
        changed_files = validator.get_recent_changes()
        
        # Run validation
        error_feedback = validator.run_incremental_check(changed_files)
        
        if error_feedback:
            # Send feedback to Claude
            print(error_feedback, file=sys.stderr)
            sys.exit(1)  # Non-blocking error
        else:
            # Success - maybe show a quick confirmation
            if os.getenv('CLAUDE_VERBOSE_HOOKS'):
                print("✅ TypeScript validation passed")
            sys.exit(0)
            
    except Exception as e:
        # Don't break Claude's flow on hook errors
        if os.getenv('CLAUDE_DEBUG_HOOKS'):
            print(f"TypeScript validator error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
```

## 3. Parallel Task Orchestration 2.0

### Enhanced `/orchestrate-graph` Command

```markdown
# Orchestrate Graph Command

Analyze task dependencies and execute in optimal parallel order.

## Implementation:

```python
# .claude/commands/orchestrate-graph.md

## Steps:

1. **Dependency Analysis**
```python
# Analyze task for dependencies
dependencies = {
    "Update auth UI": ["Create auth context", "Design auth components"],
    "Create auth context": ["Define auth types"],
    "Design auth components": ["Define auth types"],
    "Write auth tests": ["Create auth context", "Update auth UI"],
    "Update docs": []  # Can run in parallel with everything
}
```

2. **Create Execution Plan**
```
Phase 1 (Parallel):
- Agent 1: Define auth types
- Agent 2: Update docs

Phase 2 (Parallel):
- Agent 1: Create auth context
- Agent 2: Design auth components

Phase 3:
- Agent 1: Update auth UI

Phase 4:
- Agent 1: Write auth tests
```

3. **Spawn Agents**
```python
for phase in execution_plan:
    agents = []
    for task in phase.tasks:
        agent = spawn_agent(
            task=task,
            context=minimal_context,  # Only what's needed
            tools=required_tools(task)
        )
        agents.append(agent)
    
    # Wait for phase completion
    results = await Promise.all(agents)
    merge_results(results)
```

4. **Progress Dashboard**
```
🔄 Refactor Auth System Progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65%

Phase 1: ✅ Complete (2 tasks)
  └─ Define auth types ✅
  └─ Update docs ✅

Phase 2: 🔄 In Progress (2 tasks)
  └─ Create auth context ████████░░ 80%
  └─ Design auth components ███████░░░ 70%

Phase 3: ⏳ Waiting
  └─ Update auth UI

Phase 4: ⏳ Waiting
  └─ Write auth tests

Time: 3m 42s | Tokens: 45k/150k
```
```

### Token-Optimized Sub-Agent Pattern

```python
# .claude/hooks/utils/token_optimizer.py

class TokenOptimizedAgent:
    """Implements the pattern from the transcript"""
    
    def spawn_for_large_files(self, task, files):
        """Spawn agent that only returns summary"""
        
        # Prepare minimal context
        context = {
            'task': task,
            'files': [f for f in files if len(f) < 1000],  # Small files only
            'large_files': [f.name for f in files if len(f) >= 1000]
        }
        
        # Agent instructions emphasize summary
        instructions = f"""
        Task: {task}
        
        For large files, analyze and return ONLY:
        1. Key findings (bullet points)
        2. Relevant code sections (<50 lines total)
        3. Recommendations
        
        DO NOT include full file contents in response.
        """
        
        # Spawn with limited tools
        agent = spawn_agent(
            instructions=instructions,
            context=context,
            tools=['read_file', 'search_files'],  # No write tools
            max_tokens=10000  # Limit response size
        )
        
        return agent
```

## Testing Strategy

### 1. Snapshot System Tests
```bash
# Test automatic snapshots
echo "test" > test.txt
/snapshot list  # Should show new auto-snapshot

# Test rollback
/snapshot rollback 1
cat test.txt  # Should be restored

# Test cleanup
for i in {1..25}; do /snapshot create "test-$i"; done
/snapshot list  # Should show only 20
```

### 2. TypeScript Validator Tests
```typescript
// Create file with errors
/cc BadComponent
// Add: const x: string = 123
// Should see immediate error feedback

// Fix error
// Should see success message
```

### 3. Parallel Orchestration Tests
```bash
/orchestrate-graph "Create CRUD for users, posts, comments"
# Should see parallel execution phases
# Monitor token usage vs sequential
```

## Performance Metrics

### Baseline Measurements
1. **Snapshot Creation**: <100ms for <10 files
2. **TypeScript Check**: <2s incremental, <10s full
3. **Parallel Speedup**: 2-4x for independent tasks

### Monitoring
```python
# .claude/analytics/performance.py
track_metric('snapshot.create.duration', duration_ms)
track_metric('typescript.check.duration', duration_ms)
track_metric('orchestration.speedup', parallel_time / sequential_time)
```

## Rollout Plan

### Week 1-2: Foundation
1. Implement snapshot system
2. Add TypeScript validator
3. Basic testing

### Week 3-4: Integration  
1. Connect to existing hooks
2. Add commands
3. Performance optimization

### Week 5-6: Polish
1. Progress visualization
2. Error handling
3. Documentation

This implementation guide provides the technical foundation for the three highest-priority enhancements that will have the most immediate impact on developer productivity.