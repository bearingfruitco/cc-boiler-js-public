# Smart Resume - Enhanced with Auto Context Loading

Intelligently resume work with full context awareness - automatically loads relevant schemas and requirements!

## Arguments:
- $SPEED: quick|full|auto (default: auto)

## Why This Command:
- Zero memory required - finds your work automatically
- **NEW**: Auto-loads relevant context files (schemas, brands, etc.)
- Restores complete context in seconds
- Shows exactly where you left off
- Suggests next actions

## Enhanced Auto-Context Loading

### What Gets Loaded Automatically:

1. **Active Issue Requirements**
   - If working on Issue #42, loads Issue_42.json if it exists
   - Pins any requirements from the issue

2. **Relevant Context Files**
   Based on your work, automatically loads:
   - `BrandDatabase.json` - If working on brand-related features
   - `DatabaseSchema.json` - If working on models/data
   - `APIEndpoints.json` - If working on API routes
   - `ColorPalette.json` - If working on UI components

3. **Recent Context**
   - Active bugs from bug tracker
   - Current feature workflow state
   - Context anchors

## Example Output:

```
🧠 SMART RESUME - FULL CONTEXT RESTORATION
==========================================

📍 YOU ARE HERE:
Branch: feature/42-contact-form
Issue: #42 - Create contact form with 13 fields
Location: components/forms/ContactForm.tsx (65% complete)

📚 AUTO-LOADED CONTEXT:
✅ Issue_42.json - Contact form requirements (13 fields locked)
✅ BrandDatabase.json - Brand information for form options
✅ DatabaseSchema.json - Contact table structure
✅ ColorPalette.json - Design system colors

🔒 LOCKED REQUIREMENTS:
- ContactForm must have exactly 13 fields
- Required fields: firstName, lastName, email, phone...
- Corporate email validation required
- All brands must be from approved list

🕒 LAST ACTIVITY (25 min ago):
✓ Added email validation
✓ Implemented 7/13 fields
⚠️ Missing: lastName, phone, address fields

🐛 ACTIVE BUGS:
1. Form validation not triggering on blur
2. Submit button enabled when form invalid

🎯 SUGGESTED NEXT ACTIONS:
1. Add missing 6 fields to match requirement
2. Fix validation trigger issue
3. Run /review-requirements ContactForm

💡 CONTEXT TIPS:
- BrandDatabase loaded: Use only Nike, Adidas, Puma
- DatabaseSchema loaded: Match field names exactly
- Run /context-db search "phone" for phone validation rules
```

## Implementation Details:

The enhanced resume now:

1. **Scans Active Work**
   ```python
   # Detect what you're working on
   current_file = get_current_file()
   active_issue = get_active_issue()
   recent_files = get_recently_edited()
   ```

2. **Auto-Loads Relevant Context**
   ```python
   # Smart context detection
   if 'brand' in current_file.lower():
       load_context('BrandDatabase.json')
   
   if 'model' in current_file or 'schema' in current_file:
       load_context('DatabaseSchema.json')
   
   if active_issue:
       load_context(f'Issue_{active_issue}.json')
   ```

3. **Shows What's Loaded**
   - Lists all auto-loaded files
   - Shows key constraints from each
   - Highlights locked requirements

## Commands:

### Basic Resume
```bash
/sr              # Auto-detect speed
/sr quick        # Just show current state
/sr full         # Complete restoration
```

### With Context Options
```bash
/sr --no-context      # Skip auto-loading context
/sr --context=all     # Load ALL context files
/sr --show-context    # List what would be loaded
```

## Integration with Requirements

When resuming work on an issue:

1. Checks for locked requirements
2. Loads them automatically
3. Shows violations if any exist
4. Prevents starting work that would violate requirements

Example:
```
⚠️ REQUIREMENT VIOLATION DETECTED
Current implementation has 7 fields
Issue #42 requires 13 fields
Missing: lastName, phone, address, city, state, zip

Run: /review-requirements ContactForm for details
```

## Smart Detection Examples:

### Working on BrandSelector.tsx
Auto-loads:
- BrandDatabase.json (brand info)
- ColorPalette.json (brand colors)
- ValidationRules.json (if exists)

### Working on api/products/route.ts
Auto-loads:
- APIEndpoints.json (endpoint configs)
- DatabaseSchema.json (product table)
- BrandDatabase.json (valid brands)

### Working on models/Product.ts
Auto-loads:
- DatabaseSchema.json (full schema)
- ValidationRules.json (constraints)
- Migrations.json (if exists)

## Benefits:

1. **Never Miss Context** - Relevant files loaded automatically
2. **Prevent Errors** - Requirements checked on resume
3. **Faster Development** - No manual context hunting
4. **Consistency** - Always uses correct schemas/data

The goal: You run `/sr` and immediately have everything you need to continue work correctly!
