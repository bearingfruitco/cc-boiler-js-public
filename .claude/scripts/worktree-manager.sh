#!/bin/bash
# Enhanced Git Worktree Management for Claude Code Parallel Execution
# Integrates with existing Claude Code boilerplate system

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Configuration
WORKTREE_BASE=".worktrees"
MAIN_BRANCH="${WORKTREE_BRANCH:-main}"
MAX_WORKTREES=10
CLAUDE_DIR=".claude"

# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Create worktree base directory if it doesn't exist
mkdir -p "$WORKTREE_BASE"

# Functions
create_worktree() {
    local name=$1
    local task=$2
    local branch="feature/${name}"
    local path="${WORKTREE_BASE}/${name}"
    
    echo -e "${BLUE}Creating worktree: ${name}${NC}"
    
    # Check if worktree already exists
    if git worktree list | grep -q "$path"; then
        echo -e "${YELLOW}⚠️  Worktree already exists: ${name}${NC}"
        return 1
    fi
    
    # Check worktree limit
    local worktree_count=$(git worktree list | grep -v "$(pwd)" | wc -l)
    if [ $worktree_count -ge $MAX_WORKTREES ]; then
        echo -e "${RED}❌ Maximum worktrees (${MAX_WORKTREES}) reached. Clean up with: /wt-clean --old${NC}"
        return 1
    fi
    
    # Create worktree
    echo "  Creating git worktree..."
    git worktree add -b "$branch" "$path" "$MAIN_BRANCH" 2>/dev/null || {
        # Branch might already exist
        git worktree add "$path" "$branch" 2>/dev/null || {
            echo -e "${RED}❌ Failed to create worktree${NC}"
            return 1
        }
    }
    
    # Copy Claude configuration
    echo "  Copying Claude configuration..."
    if [ -d "$CLAUDE_DIR" ]; then
        cp -r "$CLAUDE_DIR" "$path/"
        
        # Create worktree-specific context
        mkdir -p "$path/$CLAUDE_DIR/context"
        
        # Create task file
        cat > "$path/$CLAUDE_DIR/context/worktree-task.md" <<EOF
# Worktree Task: ${name}

## Branch: ${branch}
## Created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
## Base: ${MAIN_BRANCH}

## Task Description
${task:-"No specific task description provided"}

## Worktree Information
This is an isolated git worktree for parallel development.
Other features are being developed in parallel in separate worktrees.

## Context
- Work independently in this worktree
- All changes are isolated to branch: ${branch}
- Other worktrees won't affect your work
- Use \`/wt-status\` to see all active worktrees
- Use \`/wt-switch\` to move between worktrees

## Next Steps
1. Run \`/sr\` to load context
2. Review the task description above
3. Begin implementation
4. Create PR when ready with \`/wt-pr ${name}\`
EOF
        
        # Create worktree config
        cat > "$path/$CLAUDE_DIR/worktree-config.json" <<EOF
{
  "worktree": {
    "name": "${name}",
    "branch": "${branch}",
    "task": "${task:-"Implement ${name} feature"}",
    "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "base": "${MAIN_BRANCH}",
    "path": "${path}",
    "status": "active"
  }
}
EOF
    fi
    
    echo -e "${GREEN}✅ Worktree created successfully${NC}"
    echo -e "${GRAY}   Path: ${path}${NC}"
    echo -e "${GRAY}   Branch: ${branch}${NC}"
    echo -e "${GRAY}   Switch with: cd ${path}${NC}"
}

list_worktrees() {
    echo -e "${BLUE}🌳 Active Worktrees${NC}"
    echo "═══════════════════════════════════════════"
    
    # Get main worktree info
    local main_path=$(git worktree list | grep -v "$WORKTREE_BASE" | awk '{print $1}')
    local main_branch=$(cd "$main_path" 2>/dev/null && git branch --show-current)
    
    echo -e "${GRAY}📍 Main${NC}"
    echo "   Path: $main_path"
    echo "   Branch: ${main_branch:-"(detached)"}"
    echo ""
    
    # List all worktrees except main
    local count=0
    while IFS= read -r line; do
        if [[ "$line" == *"$WORKTREE_BASE"* ]]; then
            local path=$(echo "$line" | awk '{print $1}')
            local name=$(basename "$path")
            local branch=$(echo "$line" | awk '{print $3}' | tr -d '[]')
            
            # Get additional info
            local task="(no task description)"
            local created="unknown"
            local config_file="$path/$CLAUDE_DIR/worktree-config.json"
            
            if [ -f "$config_file" ]; then
                task=$(grep -o '"task": "[^"]*"' "$config_file" 2>/dev/null | cut -d'"' -f4 || echo "(no task)")
                created=$(grep -o '"created": "[^"]*"' "$config_file" 2>/dev/null | cut -d'"' -f4 || echo "unknown")
            fi
            
            # Check if there are uncommitted changes
            local changes=""
            if cd "$path" 2>/dev/null && ! git diff --quiet; then
                changes="${YELLOW} [modified]${NC}"
            fi
            
            echo -e "${GREEN}📁 ${name}${NC}${changes}"
            echo "   Branch: $branch"
            echo "   Task: $task"
            echo "   Created: $created"
            echo "   Path: $path"
            echo ""
            
            ((count++))
        fi
    done < <(git worktree list)
    
    if [ $count -eq 0 ]; then
        echo -e "${GRAY}No active worktrees${NC}"
    else
        echo -e "${BLUE}Total: ${count} worktree(s)${NC}"
    fi
}

switch_worktree() {
    local name=$1
    local path="${WORKTREE_BASE}/${name}"
    
    if [ ! -d "$path" ]; then
        echo -e "${RED}❌ Worktree not found: ${name}${NC}"
        echo "Available worktrees:"
        git worktree list | grep "$WORKTREE_BASE" | awk -F'/' '{print "  - " $NF}'
        return 1
    fi
    
    echo -e "${BLUE}Switching to worktree: ${name}${NC}"
    cd "$path"
    echo -e "${GREEN}✅ Now in: $(pwd)${NC}"
    
    # Show context
    if [ -f "$CLAUDE_DIR/context/worktree-task.md" ]; then
        echo ""
        echo -e "${YELLOW}Task Context:${NC}"
        grep "^##" "$CLAUDE_DIR/context/worktree-task.md" | head -3
    fi
}

cleanup_worktree() {
    local name=$1
    local force=$2
    local path="${WORKTREE_BASE}/${name}"
    
    if [ ! -d "$path" ]; then
        echo -e "${RED}❌ Worktree not found: ${name}${NC}"
        return 1
    fi
    
    # Check for uncommitted changes
    if cd "$path" 2>/dev/null && ! git diff --quiet; then
        if [ "$force" != "--force" ]; then
            echo -e "${YELLOW}⚠️  Worktree has uncommitted changes${NC}"
            echo "Use --force to remove anyway, or commit changes first"
            return 1
        fi
    fi
    
    echo -e "${YELLOW}🧹 Cleaning up worktree: ${name}${NC}"
    
    # Return to main directory first
    cd "$(git rev-parse --show-toplevel)"
    
    # Remove worktree
    git worktree remove "$path" ${force}
    
    # Prune references
    git worktree prune
    
    echo -e "${GREEN}✅ Worktree removed${NC}"
}

cleanup_old_worktrees() {
    local days=${1:-7}
    echo -e "${YELLOW}🧹 Finding worktrees older than ${days} days${NC}"
    
    local cleaned=0
    while IFS= read -r line; do
        if [[ "$line" == *"$WORKTREE_BASE"* ]]; then
            local path=$(echo "$line" | awk '{print $1}')
            local name=$(basename "$path")
            local config_file="$path/$CLAUDE_DIR/worktree-config.json"
            
            if [ -f "$config_file" ]; then
                local created=$(grep -o '"created": "[^"]*"' "$config_file" | cut -d'"' -f4)
                if [ ! -z "$created" ]; then
                    local created_timestamp=$(date -d "$created" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$created" +%s 2>/dev/null)
                    local current_timestamp=$(date +%s)
                    local age_days=$(( ($current_timestamp - $created_timestamp) / 86400 ))
                    
                    if [ $age_days -gt $days ]; then
                        echo -e "${GRAY}  - ${name} (${age_days} days old)${NC}"
                        cleanup_worktree "$name" --force
                        ((cleaned++))
                    fi
                fi
            fi
        fi
    done < <(git worktree list)
    
    echo -e "${GREEN}✅ Cleaned up ${cleaned} old worktree(s)${NC}"
}

show_status() {
    echo -e "${BLUE}📊 Worktree Status Report${NC}"
    echo "═══════════════════════════════════════════"
    
    # Count worktrees
    local total=$(git worktree list | grep -c "$WORKTREE_BASE" || echo 0)
    local max=$MAX_WORKTREES
    
    # Disk usage
    local disk_usage="unknown"
    if command -v du > /dev/null; then
        disk_usage=$(du -sh "$WORKTREE_BASE" 2>/dev/null | awk '{print $1}' || echo "unknown")
    fi
    
    echo "Active Worktrees: ${total}/${max}"
    echo "Disk Usage: ${disk_usage}"
    echo ""
    
    # Per-worktree status
    while IFS= read -r line; do
        if [[ "$line" == *"$WORKTREE_BASE"* ]]; then
            local path=$(echo "$line" | awk '{print $1}')
            local name=$(basename "$path")
            
            # Get git status
            local changes=0
            local ahead=0
            local behind=0
            
            if cd "$path" 2>/dev/null; then
                changes=$(git status --porcelain | wc -l)
                ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)
                behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo 0)
            fi
            
            echo -e "${GREEN}${name}${NC}"
            echo "  Changes: ${changes} file(s)"
            echo "  Ahead: ${ahead} commit(s)"
            echo "  Behind: ${behind} commit(s)"
            echo ""
        fi
    done < <(git worktree list)
}

create_pr() {
    local name=$1
    local path="${WORKTREE_BASE}/${name}"
    
    if [ ! -d "$path" ]; then
        echo -e "${RED}❌ Worktree not found: ${name}${NC}"
        return 1
    fi
    
    cd "$path"
    local branch=$(git branch --show-current)
    
    # Check if there are commits to push
    if ! git rev-list @{u}..HEAD 2>/dev/null | grep -q .; then
        echo -e "${YELLOW}⚠️  No commits to push${NC}"
        return 1
    fi
    
    # Push branch
    echo -e "${BLUE}Pushing branch: ${branch}${NC}"
    git push -u origin "$branch"
    
    # Create PR using gh CLI if available
    if command -v gh > /dev/null; then
        echo -e "${BLUE}Creating pull request${NC}"
        gh pr create --fill --base "$MAIN_BRANCH"
    else
        echo -e "${YELLOW}GitHub CLI not found. Create PR manually at:${NC}"
        echo "https://github.com/$(git remote get-url origin | sed 's/.*://;s/\.git$//')/pull/new/$branch"
    fi
}

# Main command handler
case "${1:-help}" in
    create)
        shift
        while [ $# -gt 0 ]; do
            create_worktree "$1" "$2"
            shift
            shift || true
        done
        ;;
    list)
        list_worktrees
        ;;
    switch)
        switch_worktree "$2"
        ;;
    status)
        show_status
        ;;
    clean)
        if [ "$2" = "--old" ]; then
            cleanup_old_worktrees "${3:-7}"
        elif [ "$2" = "--all" ]; then
            echo -e "${YELLOW}⚠️  This will remove ALL worktrees. Continue? [y/N]${NC}"
            read -r confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                git worktree list | grep "$WORKTREE_BASE" | awk '{print $1}' | while read -r path; do
                    cleanup_worktree "$(basename "$path")" --force
                done
            fi
        else
            cleanup_worktree "$2" "$3"
        fi
        ;;
    pr)
        create_pr "$2"
        ;;
    help|*)
        echo -e "${BLUE}Git Worktree Manager for Claude Code${NC}"
        echo "══════════════════════════════════════"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  create <name> [task]    Create new worktree"
        echo "  list                    List all worktrees"
        echo "  switch <name>          Switch to worktree"
        echo "  status                 Show worktree status"
        echo "  clean <name>           Remove worktree"
        echo "  clean --old [days]     Clean worktrees older than N days (default: 7)"
        echo "  clean --all            Remove all worktrees"
        echo "  pr <name>              Create PR from worktree"
        echo "  help                   Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 create auth-feature \"Implement JWT authentication\""
        echo "  $0 switch auth-feature"
        echo "  $0 pr auth-feature"
        echo "  $0 clean auth-feature"
        ;;
esac
