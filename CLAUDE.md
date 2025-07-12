# CLAUDE.md - AI Agent Instructions with Hooks Integration

This file contains persistent instructions for Claude Code agents working on this project.
The hooks system enforces many of these rules automatically.

## 🚨 CRITICAL RULES (Enforced by Hooks)

### ALWAYS

1. **ALWAYS test before claiming fixes** - "Actually Works" protocol enforced
2. **ALWAYS use design system tokens** - Only text-size-[1-4], font-regular/semibold
3. **ALWAYS sync before editing** - GitHub pull happens automatically
4. **ALWAYS save work state** - Auto-saves every 60 seconds to GitHub
5. **ALWAYS check team activity** - Conflicts detected in real-time
6. **ALWAYS handle PII server-side** - All sensitive data processing on backend only
7. **ALWAYS encrypt PII fields** - Automatic field-level encryption for sensitive data
8. **ALWAYS audit log PII access** - Every access to sensitive data is logged

### NEVER

1. **NEVER use forbidden CSS** - text-sm, text-lg, font-bold BLOCKED
2. **NEVER use non-4px spacing** - p-5, m-7, gap-5 BLOCKED
3. **NEVER overwrite team work** - Conflicts warned before they happen
4. **NEVER lose work** - Everything backed up to GitHub gists
5. **NEVER claim "should work"** - Must verify with actual testing
6. **NEVER log PII to console** - Hook blocks console.log with sensitive data
7. **NEVER store PII client-side** - No localStorage/sessionStorage for PII
8. **NEVER put PII in URLs** - No email/phone/SSN in query parameters
9. **NEVER expose raw PII** - Always mask sensitive fields in UI
10. **NEVER skip consent** - TCPA/GDPR consent required for data collection

## 📋 Core Coding Principles

1. **Test Everything** - The "Actually Works" protocol is enforced
   - Run the code before claiming it's fixed
   - See the actual output with your own observation
   - Check for errors in console/logs
   - Would you bet $100 it works?

2. **Design System Compliance** - Automatically enforced
   - 4 font sizes only (text-size-1 through 4)
   - 2 font weights only (font-regular, font-semibold)
   - 4px spacing grid (all spacing divisible by 4)
   - 60/30/10 color distribution

3. **Evidence-Based Development** - Claims require proof
   - **NEVER say**: "best", "optimal", "faster", "secure" without evidence
   - **ALWAYS say**: "testing shows", "metrics indicate", "benchmarks reveal"
   - **Examples**:
     - ❌ "This is the best approach"
     - ✅ "Testing shows this approach reduces load time by 40%"
     - ❌ "This is more secure"
     - ✅ "Security scan confirms 0 OWASP vulnerabilities"
     - ❌ "Optimized for performance"
     - ✅ "Profiling shows 2x throughput improvement"

4. **Team Collaboration** - Hooks handle coordination
   - Auto-sync with GitHub before edits
   - Warn about conflicts with team members
   - Share knowledge automatically
   - Perfect handoffs via state persistence

## 🚀 Workflow Enhancement (v2.3.1)

### No More "Can I Edit This File?" Interruptions!

The system now auto-approves safe operations so you can work uninterrupted:

**Auto-Approved Operations:**
- ✅ Reading any file or directory
- ✅ Editing test files (/tests/, *.test.ts, *.spec.js)
- ✅ Running safe commands (npm test, lint, typecheck)
- ✅ Checking file info and searching

**Still Requires Approval:**
- 🔐 Editing production code
- 🔐 Database operations
- 🔐 Git commits and pushes
- 🔐 Installing packages

This means you can start a task, go grab coffee, and come back to completed work instead of permission prompts!

## 🤖 How Hooks Help You

### Pre-Tool-Use Hooks (Before You Edit)
- **00-auto-approve-safe-ops**: Auto-approves read operations and test edits
- **01-collab-sync**: Pulls latest changes automatically
- **02-design-check**: Blocks design violations with auto-fix
- **03-conflict-check**: Warns if team member is editing
- **04-actually-works**: Prevents untested claims
- **08-evidence-language**: Ensures claims have evidence
- **09-auto-persona**: Suggests best persona for task

### Post-Tool-Use Hooks (After You Edit)
- **01-state-save**: Backs up to GitHub every 60 seconds
- **02-metrics**: Tracks design compliance over time

### Notification Hooks (When You Need Input)
- **team-aware**: Shows who's doing what
- **smart-suggest**: Recommends relevant commands

### Stop Hooks (Session End)
- **save-state**: Final backup with summary
- **knowledge-share**: Extracts patterns for team
- **handoff-prep**: Creates handoff documentation

## 📁 Project Structure (Enforced)

```
/app              # Next.js app directory
/components
  /ui            # Base UI components
  /forms         # Form components  
  /layout        # Layout components
  /features      # Feature-specific
/lib
  /api           # API utilities
  /db            # Database utilities
/hooks           # Custom React hooks
/.claude
  /hooks         # Hook scripts
  /team          # Team coordination
  /commands      # Custom commands
```

## 🔒 Security & Data Protection

### Form Data Handling

1. **Field Registry System**
   - All fields defined in `/field-registry/`
   - Core tracking fields auto-captured
   - PII fields marked and encrypted
   - Compliance rules enforced

2. **Secure Form Creation**
   ```bash
   /create-tracked-form ContactForm --vertical=debt
   ```
   - Generates secure form with tracking
   - PII protection built-in
   - Server-side processing only
   - Audit logging included

3. **Prepopulation Rules**
   - ONLY these fields can be prepopulated from URLs:
     - utm_source, utm_medium, utm_campaign
     - gclid, fbclid, ttclid
     - partner_id, campaign_id
   - NO PII in URLs ever

4. **Data Flow Security**
   ```
   URL Params → Whitelist Check → Sanitization → Form
        ↓                                              ↓
   Block PII                                    Server-Side Only
   ```

5. **Audit Requirements**
   - Every form submission logged
   - PII access tracked
   - Consent recorded
   - Retention policies enforced

## 🧪 Testing Requirements

Before saying "fixed" or "should work":

1. **For UI Changes**
   - Actually render the component
   - Click buttons/interact with it
   - Check browser console for errors
   - Verify responsive behavior

2. **For API Changes**
   - Make the actual API call
   - Verify response format
   - Check error handling
   - Test edge cases

3. **For Logic Changes**
   - Run the specific scenario
   - Log intermediate values
   - Verify expected output
   - Test failure paths

## 📝 Documentation (Auto-Generated)

The hooks system automatically documents:
- Component patterns (when created)
- Bug fixes and solutions (when solved)
- Design compliance metrics
- Team knowledge base

Manual documentation still needed for:
- Business logic decisions
- Architecture changes
- API documentation
- Feature specifications

## 🚀 Command Enhancements

Your commands are enhanced by hooks:
- `/cc` - Validates design before creating
- `/vd` - Uses accumulated metrics
- `/checkpoint` - Auto-saves to GitHub
- `/sr` - Shows team activity
- `/fw` - Coordinates with team

## ⚡ Quick Reminders

1. **You're not alone** - Another agent may be working too
2. **Design rules are enforced** - Don't fight the system
3. **Work is auto-saved** - Focus on coding, not backing up
4. **Testing is required** - "Should work" gets flagged
5. **Knowledge is shared** - Your solutions help the team

## 🎯 The Bottom Line

The hooks system handles the mechanics so you can focus on solving problems.
But remember:

- **Untested code is just a guess**
- **Design consistency matters**
- **Team coordination prevents waste**
- **Every session teaches something**

Work with the system, not against it. The hooks are there to help you succeed.

---

*Remember: The user describing a bug for the third time isn't thinking "this AI is trying hard." They're thinking "why am I wasting my time with this tool?"*
