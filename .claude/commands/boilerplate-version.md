---
name: boilerplate-version
description: Check current boilerplate version and available updates
aliases: ["version", "check-version", "bp-version"]
---

# Check Boilerplate Version

## 🔍 Current Installation

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Claude Code Boilerplate - Version Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for VERSION file
if [ -f ".claude/VERSION" ]; then
  INSTALLED_VERSION=$(cat .claude/VERSION)
  echo "📌 Installed Version: v$INSTALLED_VERSION"
else
  echo "📌 Version file not found. Detecting by features..."
  
  # Feature-based detection
  VERSION_SCORE=0
  DETECTED_VERSION="unknown"
  
  # Check v1.0 features
  if [ -d ".claude/commands" ]; then
    VERSION_SCORE=$((VERSION_SCORE + 10))
    DETECTED_VERSION="1.0"
  fi
  
  # Check v2.0 features
  if [ -f ".claude/commands/create-prd.md" ]; then
    VERSION_SCORE=$((VERSION_SCORE + 10))
    DETECTED_VERSION="2.0"
  fi
  
  # Check v3.0 features
  if [ -f ".claude/commands/create-prp.md" ]; then
    VERSION_SCORE=$((VERSION_SCORE + 10))
    DETECTED_VERSION="3.0"
  fi
  
  # Check v3.5 features
  if [ -d ".claude/hooks" ]; then
    VERSION_SCORE=$((VERSION_SCORE + 5))
    DETECTED_VERSION="3.5"
  fi
  
  # Check v4.0 features
  if [ -d ".claude/agents" ] && [ -f ".claude/commands/orch.md" ]; then
    VERSION_SCORE=$((VERSION_SCORE + 15))
    DETECTED_VERSION="4.0"
  fi
  
  echo "📌 Detected Version: v$DETECTED_VERSION"
fi

echo ""
echo "## 📊 Feature Analysis"
echo ""

# Analyze installed features
echo "Checking installed features..."
echo ""

# Core directories
echo "Core System:"
[ -d ".claude" ] && echo "  ✓ Claude directory" || echo "  ✗ Claude directory"
[ -d ".claude/commands" ] && echo "  ✓ Commands" || echo "  ✗ Commands"
[ -d ".claude/hooks" ] && echo "  ✓ Hooks" || echo "  ✗ Hooks"
[ -d ".claude/agents" ] && echo "  ✓ Agents (v4.0)" || echo "  ✗ Agents"
[ -d ".agent-os" ] && echo "  ✓ Agent OS" || echo "  ✗ Agent OS"

echo ""
echo "Key Features:"
[ -f ".claude/commands/create-prd.md" ] && echo "  ✓ PRD System (v2.0+)" || echo "  ✗ PRD System"
[ -f ".claude/commands/create-prp.md" ] && echo "  ✓ PRP System (v3.0+)" || echo "  ✗ PRP System"
[ -f ".claude/commands/orch.md" ] && echo "  ✓ Orchestration (v4.0)" || echo "  ✗ Orchestration"
[ -f ".claude/commands/chain.md" ] && echo "  ✓ Chains (v4.0)" || echo "  ✗ Chains"
[ -d "field-registry" ] && echo "  ✓ Field Registry (v3.5+)" || echo "  ✗ Field Registry"

echo ""
echo "Development Tools:"
[ -f "biome.json" ] && echo "  ✓ Biome linting" || echo "  ✗ Biome"
[ -f "playwright.config.ts" ] && echo "  ✓ Playwright testing" || echo "  ✗ Playwright"
[ -d ".husky" ] && echo "  ✓ Git hooks" || echo "  ✗ Git hooks"

# Count commands
if [ -d ".claude/commands" ]; then
  COMMAND_COUNT=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
  echo ""
  echo "📊 Statistics:"
  echo "  • Commands: $COMMAND_COUNT"
  
  if [ -d ".claude/agents" ]; then
    AGENT_COUNT=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l)
    echo "  • Agents: $AGENT_COUNT"
  fi
  
  if [ -d ".claude/hooks" ]; then
    HOOK_COUNT=$(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
    echo "  • Hooks: $HOOK_COUNT"
  fi
fi
```

## 🔄 Version Comparison

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 📦 Latest Version: v4.0.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

LATEST_VERSION="4.0.0"

# Determine if update is available
UPDATE_AVAILABLE=false
if [ "$DETECTED_VERSION" != "4.0" ] && [ "$DETECTED_VERSION" != "unknown" ]; then
  UPDATE_AVAILABLE=true
fi

if [ "$UPDATE_AVAILABLE" = true ]; then
  echo ""
  echo "🆕 Update Available!"
  echo ""
  echo "Your version: v$DETECTED_VERSION"
  echo "Latest version: v$LATEST_VERSION"
  echo ""
  echo "## What's New in v4.0.0:"
  echo ""
  echo "✨ Multi-Agent Orchestration"
  echo "   - 31 specialized AI agents"
  echo "   - Parallel task execution"
  echo "   - Domain-specific expertise"
  echo ""
  echo "✨ Smart Workflow Chains"
  echo "   - Automated multi-step workflows"
  echo "   - 15+ pre-built chains"
  echo "   - Custom chain creation"
  echo ""
  echo "✨ Enhanced Automation"
  echo "   - Official Claude Code hook compliance"
  echo "   - Pre/post/stop hooks"
  echo "   - Performance monitoring"
  echo ""
  echo "✨ Browser Testing"
  echo "   - Playwright integration"
  echo "   - Visual regression testing"
  echo "   - E2E test automation"
  echo ""
  echo "✨ Integration System"
  echo "   - Safe integration for existing projects"
  echo "   - Version upgrades"
  echo "   - Instant rollback"
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "## 🚀 How to Upgrade"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Option 1: Upgrade existing installation"
  echo "  /upgrade-boilerplate"
  echo ""
  echo "Option 2: Selective integration"
  echo "  /integrate-boilerplate --mode=selective"
  echo ""
  echo "Option 3: Fresh installation (preserves customizations)"
  echo "  /integrate-boilerplate --mode=full"
  echo ""
  echo "All options create backups and support rollback!"
  
else
  echo ""
  echo "✅ You have the latest version!"
  echo ""
  echo "## Version History"
  echo ""
  echo "v4.0.0 (Current) - Jan 2025"
  echo "  • Multi-agent orchestration"
  echo "  • Smart workflow chains"
  echo "  • Official hook compliance"
  echo ""
  echo "v3.5 - Dec 2024"
  echo "  • Automation hooks"
  echo "  • Field registry security"
  echo ""
  echo "v3.0 - Nov 2024"
  echo "  • PRP system"
  echo "  • Enhanced PRD"
  echo ""
  echo "v2.0 - Oct 2024"
  echo "  • PRD system"
  echo "  • Task automation"
  echo ""
  echo "v1.0 - Sep 2024"
  echo "  • Initial release"
  echo "  • Basic commands"
fi
```

## 📊 Health Check

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 🏥 Installation Health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

HEALTH_SCORE=100
ISSUES=()

# Check for missing critical components
if [ ! -d ".claude/commands" ]; then
  HEALTH_SCORE=$((HEALTH_SCORE - 30))
  ISSUES+=("Missing commands directory")
fi

if [ ! -f ".claude/commands/sr.md" ]; then
  HEALTH_SCORE=$((HEALTH_SCORE - 10))
  ISSUES+=("Missing /sr command")
fi

if [ "$DETECTED_VERSION" != "4.0" ] && [ -d ".claude" ]; then
  HEALTH_SCORE=$((HEALTH_SCORE - 20))
  ISSUES+=("Not running latest version")
fi

# Check for broken symlinks or missing files
if [ -d ".claude/commands" ]; then
  BROKEN_LINKS=$(find .claude/commands -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l)
  if [ "$BROKEN_LINKS" -gt 0 ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 15))
    ISSUES+=("$BROKEN_LINKS broken command links")
  fi
fi

# Display health status
echo ""
if [ $HEALTH_SCORE -ge 90 ]; then
  echo "🟢 Health Score: $HEALTH_SCORE/100 - Excellent!"
elif [ $HEALTH_SCORE -ge 70 ]; then
  echo "🟡 Health Score: $HEALTH_SCORE/100 - Good"
elif [ $HEALTH_SCORE -ge 50 ]; then
  echo "🟠 Health Score: $HEALTH_SCORE/100 - Needs Attention"
else
  echo "🔴 Health Score: $HEALTH_SCORE/100 - Critical Issues"
fi

if [ ${#ISSUES[@]} -gt 0 ]; then
  echo ""
  echo "Issues found:"
  for issue in "${ISSUES[@]}"; do
    echo "  ⚠️ $issue"
  done
  
  echo ""
  echo "Recommended fix:"
  if [ "$DETECTED_VERSION" != "4.0" ]; then
    echo "  Run: /upgrade-boilerplate"
  else
    echo "  Run: /integrate-boilerplate --mode=selective"
  fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
