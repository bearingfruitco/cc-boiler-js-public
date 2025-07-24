# Create PRD from Existing Feature

Generate a Product Requirements Document by analyzing existing implementation.

## Usage:
- Basic: `/create-prd-from-existing dashboard`
- With analysis: `/create-prd-from-existing user-auth --analyze`
- From route: `/create-prd-from-existing /app/(dashboard)`

## Purpose:
Document existing features in PRD format for:
- Knowledge preservation
- Onboarding new team members
- Planning improvements
- Establishing baseline for changes

## Steps:

### 1. Identify Feature Scope

```bash
# Determine what files comprise this feature
FEATURE_NAME="${1:-feature}"
ANALYZE_FLAG="${2:-}"

echo "🔍 Analyzing existing feature: $FEATURE_NAME"

# Find related files
FEATURE_FILES=()

# Search in common locations
for pattern in "$FEATURE_NAME" "${FEATURE_NAME}s" "${FEATURE_NAME^}" "${FEATURE_NAME^^}"; do
  # Components
  find . -path "*/components/*" -name "*$pattern*" -type f 2>/dev/null | while read f; do
    FEATURE_FILES+=("$f")
  done
  
  # Routes/Pages
  find . -path "*/app/*" -o -path "*/pages/*" -name "*$pattern*" -type f 2>/dev/null | while read f; do
    FEATURE_FILES+=("$f")
  done
  
  # API routes
  find . -path "*/api/*" -name "*$pattern*" -type f 2>/dev/null | while read f; do
    FEATURE_FILES+=("$f")
  done
done

echo "Found ${#FEATURE_FILES[@]} related files"
```

### 2. Analyze Implementation

```bash
if [[ "$ANALYZE_FLAG" == "--analyze" ]]; then
  echo -e "\n📊 Deep Analysis Mode"
  
  # Analyze components
  echo -e "\n### Components:"
  for file in "${FEATURE_FILES[@]}"; do
    if [[ $file == *component* ]] || [[ $file == *tsx ]] || [[ $file == *jsx ]]; then
      echo "- $file"
      # Extract props interface
      grep -A 10 "interface.*Props" "$file" 2>/dev/null || true
      # Extract main component
      grep -A 5 "export.*function\|export.*const" "$file" 2>/dev/null || true
    fi
  done
  
  # Analyze API endpoints
  echo -e "\n### API Endpoints:"
  for file in "${FEATURE_FILES[@]}"; do
    if [[ $file == *api* ]]; then
      echo "- $file"
      # Extract HTTP methods
      grep -E "export.*async.*(GET|POST|PUT|DELETE|PATCH)" "$file" 2>/dev/null || true
    fi
  done
  
  # Analyze database queries
  echo -e "\n### Database Operations:"
  grep -r "supabase\|prisma\|db\." "${FEATURE_FILES[@]}" 2>/dev/null | head -20 || true
fi
```

### 3. Generate PRD Structure

```bash
# Create PRD
PRD_FILE=".claude/docs/generated/PRD-${FEATURE_NAME}-existing.md"
mkdir -p .claude/docs/generated

cat > "$PRD_FILE" << EOF
# PRD: $FEATURE_NAME (Existing Feature)

> Generated from existing implementation on $(date +%Y-%m-%d)

## 📊 Analysis Summary

- **Status**: Already Implemented ✅
- **Files Analyzed**: ${#FEATURE_FILES[@]}
- **First Implemented**: [Check git history]
- **Last Modified**: [Check git history]

## 🎯 Feature Overview

### What It Does
[Analyzed from implementation - needs human review]

### Target Users
[Inferred from UI/UX - needs validation]

### Business Value
[To be added based on business context]

## 📐 Current Implementation

### Technical Architecture
EOF

# Add file list
echo -e "\n#### Key Files:" >> "$PRD_FILE"
for file in "${FEATURE_FILES[@]}"; do
  echo "- \`$file\`" >> "$PRD_FILE"
done

cat >> "$PRD_FILE" << 'EOF'

### Component Structure
[Analyzed from component files]

### Data Flow
1. User interaction →
2. Component state →
3. API call →
4. Database operation →
5. Response handling →
6. UI update

### API Endpoints
[Extracted from API routes]

### Database Schema
[Inferred from queries]

## 🔄 Current User Flow

1. **Entry Point**: User navigates to [route/trigger]
2. **Initial State**: [Describe what user sees]
3. **Interactions**: [Available actions]
4. **Success Path**: [Happy path flow]
5. **Error Handling**: [How errors are shown]

## ✅ Existing Acceptance Criteria

Based on implementation, the feature currently:

- [ ] Allows users to [action 1]
- [ ] Validates [input type]
- [ ] Shows error when [condition]
- [ ] Saves data to [location]
- [ ] Updates UI to reflect [change]

## 🚧 Known Limitations

[Analyze from code comments, TODOs, error handling]

## 🎨 UI/UX Patterns

### Design System Compliance
- Font sizes: [Check text-size usage]
- Font weights: [Check font- usage]
- Spacing: [Check p-, m- usage]
- Colors: [Analyze color classes]

### Components Used
[List UI components found]

### Responsive Behavior
[Analyze breakpoint usage]

## 📊 Metrics & Analytics

### Current Tracking
[Search for analytics.track, eventQueue calls]

### Key Metrics
- Usage: [If tracked]
- Success rate: [If tracked]
- Error rate: [If tracked]

## 🔧 Technical Debt

### Code Quality Issues
[Based on analysis]

### Missing Features
[Based on TODOs and comments]

### Performance Considerations
[Based on implementation patterns]

## 📈 Improvement Opportunities

### Quick Wins
1. [Based on code analysis]
2. [Based on patterns]

### Major Enhancements
1. [Architectural improvements]
2. [Feature additions]

### Migration Needs
- [ ] Design system compliance
- [ ] TypeScript strict mode
- [ ] Test coverage
- [ ] Accessibility

## 🧪 Testing Status

### Existing Tests
[Search for .test.tsx, .spec.ts files]

### Test Coverage
- Unit tests: [Present/Missing]
- Integration tests: [Present/Missing]
- E2E tests: [Present/Missing]

### Recommended Tests
1. [Based on critical paths]
2. [Based on edge cases]

## 📚 Documentation Status

### Existing Docs
- Code comments: [Analyze]
- README sections: [Check]
- Storybook: [Check]

### Needed Documentation
1. User guide
2. API documentation
3. Architecture diagram

## 🔄 Dependencies

### Internal Dependencies
[Components and utilities used]

### External Dependencies
[NPM packages specific to this feature]

### Impact Analysis
Features that depend on this:
- [Search for imports]

## 🎯 Success Metrics (To Define)

### User Metrics
- [ ] [Metric 1]
- [ ] [Metric 2]

### Technical Metrics
- [ ] Performance benchmarks
- [ ] Error rates
- [ ] Test coverage target

## 📋 Migration to Modern Standards

### Phase 1: Documentation ✅
- [x] Generate this PRD
- [ ] Review and validate with team
- [ ] Add business context

### Phase 2: Compliance
- [ ] Migrate to strict design system
- [ ] Add comprehensive tests
- [ ] Improve error handling

### Phase 3: Enhancement
- [ ] Address technical debt
- [ ] Add missing features
- [ ] Optimize performance

---

## Notes

This PRD was reverse-engineered from existing code. Please review and update:
1. Business context and value
2. Success metrics
3. User personas
4. Actual usage data
EOF

echo -e "\n✅ PRD created: $PRD_FILE"
```

### 4. Generate Improvement Tasks

```bash
# Create a companion improvements file
IMPROVEMENTS_FILE=".claude/docs/generated/IMPROVEMENTS-${FEATURE_NAME}.md"

cat > "$IMPROVEMENTS_FILE" << EOF
# Improvement Plan: $FEATURE_NAME

Based on code analysis, here are recommended improvements:

## 🚨 Critical Issues

### Design System Violations
\`\`\`bash
# Run to see all violations:
/vd ${FEATURE_FILES[0]}
\`\`\`

### Missing Error Handling
[Analyzed from code]

### Accessibility Gaps
[Based on ARIA usage]

## 🎯 Quick Wins (< 2 hours each)

1. **Standardize Typography**
   - Replace text-sm → text-size-3
   - Replace font-bold → font-semibold
   
2. **Add Loading States**
   - Implement loading skeletons
   - Add disabled states during async operations

3. **Improve Error Messages**
   - User-friendly error text
   - Clear next actions

## 📈 Medium Improvements (2-8 hours)

1. **Add Comprehensive Tests**
   \`\`\`bash
   /prd-tests $FEATURE_NAME
   \`\`\`

2. **Implement Event Tracking**
   - Add form analytics
   - Track user interactions
   - Monitor errors

3. **Enhance Accessibility**
   - Add ARIA labels
   - Ensure keyboard navigation
   - Test with screen reader

## 🏗️ Major Enhancements (8+ hours)

1. **Performance Optimization**
   - Implement lazy loading
   - Add caching layer
   - Optimize queries

2. **Feature Extensions**
   [Based on TODOs and comments]

3. **Architecture Improvements**
   - Separate concerns
   - Extract reusable hooks
   - Implement proper state management

## 📋 Implementation Commands

\`\`\`bash
# Start improvement work
/fw start improvement-$FEATURE_NAME

# Create fresh PRD for enhancements
/prd ${FEATURE_NAME}-v2

# Generate tasks
/gt ${FEATURE_NAME}-v2

# Process with validation
/pt ${FEATURE_NAME}-v2
\`\`\`
EOF

echo "📋 Improvements documented: $IMPROVEMENTS_FILE"
```

### 5. Integration with Existing Workflows

```bash
# Update context for smart resume
if [ -f ".claude/context/features.json" ]; then
  # Add to known features
  jq --arg feature "$FEATURE_NAME" '. + {($feature): {"status": "documented", "prd": "'$PRD_FILE'"}}' \
    .claude/context/features.json > .claude/context/features.json.tmp
  mv .claude/context/features.json.tmp .claude/context/features.json
else
  # Create features context
  echo '{"'$FEATURE_NAME'": {"status": "documented", "prd": "'$PRD_FILE'"}}' > .claude/context/features.json
fi

# Create task to review
echo "REVIEW: Generated PRD for $FEATURE_NAME" >> .claude/bugs/review-needed.md
echo "- [ ] Add business context" >> .claude/bugs/review-needed.md
echo "- [ ] Validate technical analysis" >> .claude/bugs/review-needed.md
echo "- [ ] Prioritize improvements" >> .claude/bugs/review-needed.md
```

### 6. Summary Output

```bash
echo -e "\n## 📄 PRD Generation Complete!"
echo ""
echo "### Created Documents:"
echo "1. PRD: $PRD_FILE"
echo "2. Improvements: $IMPROVEMENTS_FILE"
echo ""
echo "### Next Steps:"
echo "1. Review generated PRD for accuracy"
echo "2. Add business context and metrics"
echo "3. Validate with team/stakeholders"
echo "4. Use improvement plan for backlog"
echo ""
echo "### Follow-up Commands:"
echo "- \`/vd $FEATURE_NAME\` - Check design compliance"
echo "- \`/prd-tests $FEATURE_NAME\` - Generate test suite"
echo "- \`/grade --existing $FEATURE_NAME\` - Score current implementation"
echo "- \`/fw start improve-$FEATURE_NAME\` - Begin improvements"
```

## Examples:

```bash
# Document a dashboard feature
/create-prd-from-existing dashboard

# Deep analysis of auth system
/create-prd-from-existing auth --analyze

# Document API endpoint
/create-prd-from-existing user-api

# From specific route
/create-prd-from-existing "(dashboard)"
```

## Integration:

- Works with `/analyze-existing` for full project documentation
- Feeds into `/grade` for implementation scoring
- Enables `/fw start` with context of existing code
- Supports `/migrate-to-strict-design` with baseline