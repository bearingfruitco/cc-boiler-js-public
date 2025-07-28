# Smart Resume - Enhanced with Standards

Intelligently resume work with full context awareness including centralized standards.

## Arguments:
- $SPEED: quick|full|auto (default: auto)

## Why This Command:
- Zero memory required - finds your work automatically
- Loads global standards for consistency
- Restores complete context in seconds
- Shows exactly where you left off
- Suggests next actions

## Steps:

### 0. Load Global Standards (NEW)
Always load centralized standards first:

```bash
# Load global standards if they exist
if [ -d ".agent-os/standards" ]; then
  echo "## 📚 Loading Standards"
  echo ""
  
  for file in .agent-os/standards/*.md; do
    if [ -f "$file" ]; then
      filename=$(basename "$file")
      echo "✓ Loaded: $filename"
    fi
  done
  echo ""
fi
```

### Speed: AUTO (Default)
Automatically determines what you need:

```bash
# 1. Check time since last work
LAST_MODIFIED=$(find .claude/context/current.md -mmin -60 2>/dev/null)

if [ -z "$LAST_MODIFIED" ]; then
  # Context is old, do full resume
  SPEED="full"
else
  # Recent context, quick resume
  SPEED="quick"
fi
```

### Speed: QUICK
For resuming after short breaks (<1 hour):

```bash
# 1. Show Current Location
echo "## 📍 You Are Here"
echo ""

# Get from context file
BRANCH=$(git branch --show-current)
ISSUE=$(echo $BRANCH | grep -oE '[0-9]+' | head -1)
CURRENT_FILE=$(grep "Location:" .claude/context/current.md | head -1 | cut -d' ' -f2)

echo "Branch: $BRANCH"
echo "Issue: #$ISSUE"
echo "File: $CURRENT_FILE"

# 2. Show Last Activity
echo -e "\n## 🕒 Last Activity"
LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s (%cr)")
echo "Last commit: $LAST_COMMIT"

# 3. Show Current Task
echo -e "\n## 📋 Current Task"
if [ -f ".claude/state/current-task.json" ]; then
  TASK=$(jq -r '.title' .claude/state/current-task.json)
  PROGRESS=$(jq -r '.progress' .claude/state/current-task.json)
  echo "Task: $TASK"
  echo "Progress: $PROGRESS%"
fi

# 4. Context Summary
echo -e "\n## 📚 Active Context"
echo "- PRD: $(ls .claude/context/prd-*.md 2>/dev/null | wc -l) files"
echo "- Requirements: $(ls .claude/requirements/*.json 2>/dev/null | wc -l) locked"
echo "- Research: $(ls .claude/research/*.md 2>/dev/null | wc -l) docs"
echo "- Standards: $(ls .agent-os/standards/*.md 2>/dev/null | wc -l) files"
```

### Speed: FULL
For starting fresh or after long breaks:

```bash
# Everything from QUICK plus:

# 5. Load All Context Files
echo -e "\n## 📂 Loading Full Context"

# Load PRDs
for prd in .claude/context/prd-*.md; do
  if [ -f "$prd" ]; then
    echo "✓ PRD: $(basename $prd)"
  fi
done

# Load locked requirements
for req in .claude/requirements/*.json; do
  if [ -f "$req" ]; then
    echo "✓ Requirement: $(basename $req .json)"
  fi
done

# Load standards
for std in .agent-os/standards/*.md; do
  if [ -f "$std" ]; then
    echo "✓ Standard: $(basename $std)"
  fi
done

# 6. Show Task Progress
echo -e "\n## ✅ Task Progress"
if [ -f ".task-ledger.md" ]; then
  TOTAL=$(grep -c "^- \[" .task-ledger.md)
  DONE=$(grep -c "^- \[x\]" .task-ledger.md)
  PERCENT=$((DONE * 100 / TOTAL))
  echo "Progress: $DONE/$TOTAL tasks ($PERCENT%)"
  
  # Show next 3 tasks
  echo -e "\nNext tasks:"
  grep "^- \[ \]" .task-ledger.md | head -3
fi

# 7. Show Active Bugs
echo -e "\n## 🐛 Active Bugs"
if [ -d ".claude/bugs" ]; then
  BUG_COUNT=$(ls .claude/bugs/*.json 2>/dev/null | wc -l)
  echo "Active bugs: $BUG_COUNT"
  
  if [ $BUG_COUNT -gt 0 ]; then
    for bug in $(ls .claude/bugs/*.json | head -3); do
      TITLE=$(jq -r '.title' "$bug")
      echo "- $TITLE"
    done
  fi
fi

# 8. Check Branch Health
echo -e "\n## 🌿 Branch Health"
COMMITS_AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
COMMITS_BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")

echo "- Ahead of main: $COMMITS_AHEAD commits"
echo "- Behind main: $COMMITS_BEHIND commits"

if [ $COMMITS_BEHIND -gt 10 ]; then
  echo "⚠️  Consider syncing with main: /sync-main"
fi
```

### Next Actions
Based on context, suggest next steps:

```bash
echo -e "\n## 🎯 Suggested Next Actions"

# Check various states and suggest
if [ -f ".claude/state/current-task.json" ]; then
  echo "1. Continue current task: /pt"
elif [ $(grep -c "^- \[ \]" .task-ledger.md 2>/dev/null || echo 0) -gt 0 ]; then
  echo "1. Process next task: /pt"
elif [ -f ".claude/context/prd-*.md" ]; then
  echo "1. Generate tasks from PRD: /gt [feature]"
else
  echo "1. Start new feature: /fw start [issue#]"
fi

# Always suggest these
echo "2. Check task status: /ts"
echo "3. Validate design: /vd"
echo "4. Run tests: /tr"
```

## Context Awareness:

The command now:
1. Loads global standards from `.agent-os/standards/`
2. Shows standards in context summary
3. Makes standards available for all subsequent commands
4. Falls back gracefully if standards don't exist

## Integration:

Works seamlessly with:
- Existing context management
- Task ledger system
- Bug tracking
- Branch awareness
- All other commands
