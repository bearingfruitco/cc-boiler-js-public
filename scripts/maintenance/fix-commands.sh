#!/bin/bash
# Fix command duplicates and create alias symlinks

echo "🔧 Fixing Claude Code command structure..."

cd /Users/shawnsmith/dev/bfc/boilerplate/.claude/commands

# Archive duplicates
mkdir -p _archived_duplicates

# 1. Smart Resume - keep the main one
mv smart-resume-enhanced.md _archived_duplicates/ 2>/dev/null
mv smart-resume-standards.md _archived_duplicates/ 2>/dev/null

# 2. Feature Workflow - keep the main one
mv feature-workflow-enhanced.md _archived_duplicates/ 2>/dev/null
mv feature-workflow-start-enhanced.md _archived_duplicates/ 2>/dev/null

# 3. Stage Validate - keep enhanced
mv stage-validate-grade.md _archived_duplicates/ 2>/dev/null
mv stage-validate-grade-enhanced.md stage-validate-grade.md 2>/dev/null

# 4. TDD Workflow - keep enhanced
mv tdd-workflow.md _archived_duplicates/ 2>/dev/null
mv tdd-workflow-enhanced.md tdd-workflow.md 2>/dev/null

# 5. Init Project - keep enhanced
mv init-project.md _archived_duplicates/ 2>/dev/null
mv init-project-enhanced.md init-project.md 2>/dev/null

# 6. Generate Issues - keep enhanced
mv generate-issues.md _archived_duplicates/ 2>/dev/null
mv generate-issues-enhanced.md generate-issues.md 2>/dev/null

# Create sr.md as an alias for smart-resume
cat > sr.md << 'EOF'
# Smart Resume Alias

$ARGUMENTS

This is an alias for /smart-resume. It will restore your context from previous sessions.
EOF

# Create common aliases as actual command files
cat > cc.md << 'EOF'
# Create Component Alias

/create-component $ARGUMENTS
EOF

cat > vd.md << 'EOF'
# Validate Design Alias

/validate-design $ARGUMENTS
EOF

cat > prd.md << 'EOF'
# Create PRD Alias

/create-prd $ARGUMENTS
EOF

cat > fw.md << 'EOF'
# Feature Workflow Alias

/feature-workflow $ARGUMENTS
EOF

cat > cp.md << 'EOF'
# Checkpoint Alias

/checkpoint $ARGUMENTS
EOF

cat > gt.md << 'EOF'
# Generate Tasks Alias

/generate-tasks $ARGUMENTS
EOF

echo "✅ Commands consolidated"
echo "✅ Alias commands created"

# Update command registry
cd ..
cat > command-registry-updated.json << 'EOF'
{
  "primary_commands": {
    "smart-resume": "Restore context from previous sessions",
    "create-component": "Create a new component with design system",
    "validate-design": "Validate design system compliance",
    "create-prd": "Create Product Requirements Document",
    "feature-workflow": "Start feature development workflow",
    "checkpoint": "Save current work state",
    "generate-tasks": "Generate tasks from PRD",
    "init-project": "Initialize new project",
    "stage-validate-grade": "Grade implementation against PRD",
    "tdd-workflow": "Test-driven development workflow",
    "generate-issues": "Generate GitHub issues from PRD"
  },
  "aliases": {
    "sr": "smart-resume",
    "cc": "create-component",
    "vd": "validate-design",
    "prd": "create-prd",
    "fw": "feature-workflow",
    "cp": "checkpoint",
    "gt": "generate-tasks"
  }
}
EOF

echo "📝 Updated command registry"
echo ""
echo "Commands fixed:"
echo "- Removed duplicate enhanced/standards versions"
echo "- Created direct alias command files (sr.md, cc.md, etc.)"
echo "- Updated registry with primary commands"
echo ""
echo "Now /sr should work directly in Claude Code!"
