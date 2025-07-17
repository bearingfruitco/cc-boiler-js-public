# Feature Workflow - Enhanced with Auto Requirements

Orchestrates issue-based development with automatic requirement extraction and context loading.

## Arguments:
- $ACTION: start|validate|complete
- $ISSUE_NUMBER: GitHub issue number

## Why This Command:
GitHub MCP handles Git operations, but doesn't:
- Extract and lock requirements from issues
- Auto-load relevant context files
- Enforce design system rules
- Create issue-based workflows

## Enhanced Features:

### NEW: Automatic Requirement Extraction
When starting work on an issue, the command now:
1. Extracts requirements from issue description
2. Creates locked requirement file
3. Loads relevant context files
4. Sets up enforcement hooks

## Steps:

### Action: START

1. **Get Issue & Extract Requirements**
   ```typescript
   // Get issue from GitHub
   const issue = await github.getIssue(ISSUE_NUMBER);
   
   // Extract requirements automatically
   const requirements = extractRequirements(issue);
   
   // Lock requirements
   await createLockedRequirement({
     source: { type: 'github_issue', reference: ISSUE_NUMBER },
     requirements: requirements
   });
   ```

2. **Auto-Load Relevant Context**
   Based on issue content, automatically loads:
   - Related schemas (if mentions database/model)
   - Brand database (if mentions brands)
   - API configs (if mentions endpoints)
   - Design system (if UI work)

3. **Create Worktree with Context**
   ```bash
   BRANCH_NAME="feature/${ISSUE_NUMBER}-${SLUG}"
   
   # Create with pre-loaded context
   echo "Issue #${ISSUE_NUMBER} Requirements:" > .context
   echo "- ${REQUIREMENT_SUMMARY}" >> .context
   ```

## Example: Starting Issue #42

```bash
/fw start 42
```

Output:
```
🚀 STARTING FEATURE WORKFLOW FOR ISSUE #42
=========================================

📋 Issue: Create contact form with 13 fields
👤 Assignee: @shawnsmith

📊 EXTRACTED REQUIREMENTS:
- Component: ContactForm
- Field Count: 13 (LOCKED)
- Required Fields: firstName, lastName, email, phone...
- Validation: Corporate email only
- Design: Mobile-first responsive

✅ Created: .claude/requirements/locked/Issue_42.json

📚 AUTO-LOADED CONTEXT:
- DatabaseSchema.json (contact table structure)
- BrandDatabase.json (for company field options)
- ValidationRules.json (email/phone patterns)

🔒 REQUIREMENTS LOCKED:
Any attempt to deviate from 13 fields will be blocked

🌳 Worktree: feature/42-contact-form
📍 Location: ../project-worktrees/feature/42-contact-form

🎯 NEXT STEPS:
1. cd ../project-worktrees/feature/42-contact-form
2. /prd ContactForm  # Will include locked requirements
3. /cc ContactForm   # Will enforce 13 fields
```

## Requirement Extraction Rules:

### What Gets Extracted:
1. **Numeric Requirements**
   - "13 fields" → `fields.count: 13`
   - "minimum 8 characters" → `validation.minLength: 8`
   - "max 10MB" → `constraints.maxSize: 10485760`

2. **List Requirements**
   - "fields: name, email, phone" → `fields.names: ["name", "email", "phone"]`
   - "support Nike, Adidas" → `brands: ["Nike", "Adidas"]`

3. **Boolean Requirements**
   - "required field" → `required: true`
   - "mobile responsive" → `responsive: true`

4. **Feature Requirements**
   - "email validation" → `features: ["email_validation"]`
   - "autocomplete address" → `features: ["address_autocomplete"]`

### Issue Format Support:

The extractor understands common issue formats:

**Checklist Format:**
```markdown
- [ ] Add 13 form fields
- [ ] Include email validation
- [ ] Mobile responsive
```

**Requirements Section:**
```markdown
## Requirements
- Fields: 13 total
- Required: all except company
- Validation: corporate email only
```

**User Story Format:**
```markdown
As a user, I need a contact form with 13 fields
So that I can provide complete information
```

## Smart Context Detection:

Based on issue content, loads relevant files:

| Issue Contains | Auto-Loads |
|----------------|------------|
| "brand", "Nike", "Adidas" | BrandDatabase.json |
| "database", "table", "schema" | DatabaseSchema.json |
| "API", "endpoint", "route" | APIEndpoints.json |
| "color", "design", "style" | ColorPalette.json |
| "product", "SKU", "catalog" | ProductCatalog.json |

## Validation on Complete:

```bash
/fw complete 42
```

Before completing:
1. Runs `/review-requirements` automatically
2. Checks all locked requirements met
3. Validates against original issue
4. Only allows completion if 100% compliant

## Integration with Other Commands:

### With PRD Generation:
```bash
/fw start 42
/prd ContactForm  # PRD includes Issue #42 requirements
```

### With Component Creation:
```bash
/fw start 42
/cc ContactForm  # Component enforces Issue #42 requirements
```

### With Grading:
```bash
/fw start 42
# ... work ...
/grade --requirements  # Grades against Issue #42
```

## Benefits:

1. **Never Drift from Issues** - Requirements locked from start
2. **Automatic Context** - No manual file hunting
3. **Enforced Compliance** - Can't complete until requirements met
4. **Seamless Workflow** - Everything connected to issue

The goal: Start with an issue, automatically have all requirements locked and context loaded, preventing any drift from the original specification!
