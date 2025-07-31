# Analyze Existing Codebase

Drop into any existing project and generate comprehensive Agent OS + Boilerplate documentation.

## Arguments:
- $MODE: full|quick|standards-only (default: full)

## Purpose:
- Analyze existing codebase structure and patterns
- Generate mission, roadmap, and decisions documentation
- Detect tech stack and coding patterns
- Create PRDs for existing features
- Set up boilerplate system in existing project

## Steps:

### 1. Project Analysis Phase

```bash
echo "## 🔍 Analyzing Existing Codebase"
echo ""

# Detect project type
if [ -f "package.json" ]; then
  PROJECT_TYPE="node"
  FRAMEWORK=$(jq -r '.dependencies | keys[] | select(. == "next" or . == "react" or . == "vue" or . == "angular")' package.json | head -1)
elif [ -f "Gemfile" ]; then
  PROJECT_TYPE="ruby"
  FRAMEWORK=$(grep -E "gem ['\"]rails['\"]" Gemfile && echo "rails" || echo "ruby")
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="python"
  FRAMEWORK=$(grep -E "django|flask|fastapi" requirements.txt 2>/dev/null | head -1)
fi

echo "Project Type: $PROJECT_TYPE"
echo "Framework: $FRAMEWORK"
```

### 2. Codebase Structure Analysis

```bash
# Analyze directory structure
echo -e "\n## 📁 Project Structure"

# Check for common patterns
STRUCTURE_TYPE="unknown"
if [ -d "app" ] && [ -d "components" ]; then
  STRUCTURE_TYPE="nextjs-app-router"
elif [ -d "src/pages" ]; then
  STRUCTURE_TYPE="nextjs-pages"
elif [ -d "src/components" ] && [ -d "src/App" ]; then
  STRUCTURE_TYPE="react-spa"
fi

echo "Structure Type: $STRUCTURE_TYPE"

# Count existing components
COMPONENT_COUNT=$(find . -name "*.tsx" -o -name "*.jsx" | grep -i component | wc -l)
echo "Existing Components: $COMPONENT_COUNT"

# Detect design system
DESIGN_SYSTEM="unknown"
if grep -q "tailwind" package.json 2>/dev/null; then
  DESIGN_SYSTEM="tailwind"
  # Check if using our strict system
  if grep -q "text-size-[1-4]" $(find . -name "*.tsx" -o -name "*.jsx" | head -5) 2>/dev/null; then
    DESIGN_SYSTEM="tailwind-strict"
  fi
elif grep -q "styled-components" package.json 2>/dev/null; then
  DESIGN_SYSTEM="styled-components"
fi

echo "Design System: $DESIGN_SYSTEM"
```

### 3. Feature Detection

```bash
echo -e "\n## 🎯 Detected Features"

# Analyze routes/pages to understand features
FEATURES=()

# Next.js App Router
if [ -d "app" ]; then
  for dir in app/*/; do
    if [ -d "$dir" ] && [ "$dir" != "app/api/" ]; then
      feature=$(basename "$dir" | sed 's/[()]//g')
      FEATURES+=("$feature")
    fi
  done
fi

# Next.js Pages Router
if [ -d "pages" ]; then
  for file in pages/*.{tsx,jsx,js}; do
    if [ -f "$file" ] && [[ ! "$file" =~ _app|_document|api ]]; then
      feature=$(basename "$file" .tsx | sed 's/\..*//')
      FEATURES+=("$feature")
    fi
  done
fi

echo "Found ${#FEATURES[@]} features:"
printf ' - %s\n' "${FEATURES[@]}"
```

### 4. Generate Agent OS Structure

```bash
echo -e "\n## 📚 Creating Agent OS Documentation"

# Create directories
mkdir -p .agent-os/product
mkdir -p .agent-os/specs
mkdir -p .claude/commands
mkdir -p .claude/context
```

#### 4.1 Generate Mission Document

```markdown
# Create .agent-os/product/mission.md

cat > .agent-os/product/mission.md << 'EOF'
# Product Mission

## Elevator Pitch
[Analyzed from package.json description and README]

## Target Users
[Inferred from features and UI patterns]

## Core Problem
[Deduced from feature set]

## Our Solution
[Based on implemented features]

## Success Metrics
[To be defined - analyze analytics integration]

## Detected Features
EOF

# Add detected features
for feature in "${FEATURES[@]}"; do
  echo "- $feature" >> .agent-os/product/mission.md
done
```

#### 4.2 Generate Roadmap

```markdown
# Create .agent-os/product/roadmap.md

cat > .agent-os/product/roadmap.md << 'EOF'
# Product Roadmap

## Phase 0: Already Implemented ✅
Based on codebase analysis, these features are complete:

EOF

# Add completed features
for feature in "${FEATURES[@]}"; do
  echo "- [x] $feature" >> .agent-os/product/roadmap.md
done

cat >> .agent-os/product/roadmap.md << 'EOF'

## Phase 1: Immediate Improvements 🚀
Based on analysis, these areas need attention:

- [ ] Design system standardization
- [ ] Test coverage improvement
- [ ] Performance optimization
- [ ] Accessibility audit

## Phase 2: Feature Enhancements 📈
[To be planned based on business goals]

## Phase 3: Scale & Optimize 🎯
[To be planned based on growth]
EOF
```

#### 4.3 Generate Tech Stack Documentation

```bash
# Create .agent-os/product/tech-stack.md
echo "# Project Tech Stack" > .agent-os/product/tech-stack.md
echo "" >> .agent-os/product/tech-stack.md
echo "## Detected Stack" >> .agent-os/product/tech-stack.md

# Parse package.json for dependencies
if [ -f "package.json" ]; then
  echo "### Core Framework" >> .agent-os/product/tech-stack.md
  jq -r '.dependencies | to_entries[] | "- \(.key): \(.value)"' package.json | grep -E "next|react|vue|angular" >> .agent-os/product/tech-stack.md
  
  echo "### UI/Styling" >> .agent-os/product/tech-stack.md
  jq -r '.dependencies | to_entries[] | "- \(.key): \(.value)"' package.json | grep -E "tailwind|styled|emotion|css" >> .agent-os/product/tech-stack.md
  
  echo "### State/Data" >> .agent-os/product/tech-stack.md
  jq -r '.dependencies | to_entries[] | "- \(.key): \(.value)"' package.json | grep -E "redux|zustand|react-query|swr" >> .agent-os/product/tech-stack.md
fi
```

### 5. Generate Boilerplate Integration

```bash
echo -e "\n## 🔧 Integrating Boilerplate System"

# Check if boilerplate system exists
if [ ! -d ".claude" ]; then
  echo "Setting up Claude Code Boilerplate system..."
  
  # Create essential structure
  mkdir -p .claude/{commands,hooks,context,state,bugs,research}
  
  # Copy essential commands from boilerplate
  cp ~/.claude/commands/{smart-resume,create-component,validate-design}.md .claude/commands/
  
  # Create project-specific CLAUDE.md
  cat > .claude/CLAUDE.md << 'EOF'
# Claude Code Context for This Project

## Project Analysis Complete ✅
- See .agent-os/product/ for full documentation
- Tech stack detected and documented
- Existing features mapped to roadmap

## Standards
- Global: ~/.agent-os/standards/
- Project: .agent-os/standards/ (if customized)

## Quick Commands
- /sr - Resume with full context
- /create-component - With design validation
- /vd - Validate design compliance
EOF
fi
```

### 6. Create Migration Guide

```bash
cat > .agent-os/MIGRATION_GUIDE.md << 'EOF'
# Migration Guide: Existing Project → Agent OS + Boilerplate

## What We Found
- Project Type: ${PROJECT_TYPE}
- Framework: ${FRAMEWORK}
- Structure: ${STRUCTURE_TYPE}
- Components: ${COMPONENT_COUNT}
- Features: ${#FEATURES[@]}

## What We Created
1. **Agent OS Documentation**
   - ✅ Mission document with detected features
   - ✅ Roadmap with Phase 0 (completed work)
   - ✅ Tech stack analysis
   - ✅ Decisions log (empty, ready for use)

2. **Boilerplate Integration**
   - ✅ Basic command structure
   - ✅ Context management setup
   - 🔄 Design system migration needed

## Next Steps

### 1. Review Generated Documentation
- Check .agent-os/product/mission.md
- Verify detected features in roadmap.md
- Update tech-stack.md with missing details

### 2. Standardize Design System
Run: /migrate-to-strict-design

### 3. Create PRDs for Existing Features
For each major feature, run:
/create-prd-from-existing [feature-name]

### 4. Set Up Validation
- Enable design system hooks
- Configure pre-commit hooks
- Set up CI/CD validation

### 5. Begin Enhancement Work
- Start with Phase 1 roadmap items
- Use full boilerplate workflow for new features
EOF
```

### 7. Hook Into Existing Workflows

```bash
# Update chains to include analyze capability
if [ -f ".claude/chains.json" ]; then
  # Add new chain for existing projects
  jq '. + {
    "analyze-and-setup": {
      "description": "Analyze existing project and set up full system",
      "steps": [
        "/analyze-existing full",
        "/sr",
        "Review .agent-os/product/mission.md",
        "Update roadmap with business goals",
        "/migrate-to-strict-design"
      ]
    }
  }' .claude/chains.json > .claude/chains.json.tmp
  mv .claude/chains.json.tmp .claude/chains.json
fi
```

### 9. Next Steps Integration

```bash
echo -e "\n## ✍️ Next Steps for Integration"
echo ""
echo "Now that analysis is complete, you have several options:"
echo ""
echo "### Option 1: Smart Integration (Recommended)"
echo "Use the new conflict-aware integration:"
echo ""
echo "  /integrate-boilerplate --mode=full"
echo ""
echo "This will:"
echo "- Preserve your existing CLAUDE.md"
echo "- Keep all your custom commands"
echo "- Merge hooks intelligently"
echo "- Add boilerplate features without breaking anything"
echo ""
echo "### Option 2: Selective Integration"
echo "Choose specific features:"
echo ""
echo "  /integrate-boilerplate --mode=selective"
echo ""
echo "### Option 3: Side-by-Side Testing"
echo "Install separately for testing:"
echo ""
echo "  /integrate-boilerplate --mode=sidecar"
echo ""
echo "### Always Safe"
echo "- Automatic backup before any changes"
echo "- Instant rollback with /integration-rollback"
echo "- Dry run mode: /integrate-boilerplate --dry-run"
```

## Integration Points:

1. **Works with existing commands**:
   - Feeds into `/sr` for context loading
   - Enables `/create-component` with proper context
   - Allows `/vd` to check against detected patterns

2. **Enhances workflows**:
   - PRD generation understands existing code
   - PRP creation references implemented patterns
   - Task generation avoids recreating existing features

3. **Hooks compatibility**:
   - Design validator knows current state
   - Import validator understands project structure
   - Truth enforcer protects existing implementations

4. **Chain integration**:
   - New "analyze-and-setup" chain for onboarding
   - Existing chains work with generated context
   - Smart resume includes analysis results
