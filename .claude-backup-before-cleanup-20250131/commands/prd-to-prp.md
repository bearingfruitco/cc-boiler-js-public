---
name: prd-to-prp
aliases: [convert-to-prp, prp-convert, enhance-prd]
description: Convert existing PRD to a comprehensive PRP with automation capability
category: PRPs
---

# Convert PRD to PRP: $ARGUMENTS

Transform an existing PRD into a comprehensive PRP (Product Requirement Prompt) that enables one-pass implementation and automation.

## Process:

1. **Load Existing PRD**
   - Find PRD in docs/prd/ or context
   - Extract core requirements
   - Identify gaps for automation

2. **Research Enhancement Phase**
   
   ### Spawn Research Agents
   ```
   /spawn backend "Find implementation patterns for $ARGUMENTS"
   /spawn security "Identify security concerns for $ARGUMENTS"
   /spawn research "Find best practices and gotchas for $ARGUMENTS"
   ```
   
   ### Analyze Codebase
   - Find similar implementations
   - Extract successful patterns
   - Identify reusable components

3. **Add PRP-Specific Sections**

   ### All Needed Context
   ```yaml
   # From codebase analysis
   - file: src/similar_feature.py
     pattern: Authentication flow pattern
     gotcha: Must use async context manager
   
   # From research
   - url: https://docs.example.com/api
     why: Rate limiting details
     critical: 10 requests/second max
   
   # From doc cache
   - docfile: PRPs/ai_docs/patterns.md
     why: Established patterns to follow
   ```

   ### Known Gotchas
   - Library-specific issues discovered
   - Performance bottlenecks identified
   - Security considerations found
   - Integration challenges

   ### Implementation Blueprint
   - Detailed task breakdown
   - Exact file structure
   - Code patterns to follow
   - Dependencies between tasks

   ### Validation Loops
   - Level 1: Syntax (automatic via hooks)
   - Level 2: Unit tests 
   - Level 3: Integration tests
   - Level 4: Production readiness

4. **Link to Requirements**
   
   If PRD references GitHub issues:
   ```
   Pinned Requirements: #42
   Context Anchors: 
   - "Must support 1000 concurrent users"
   - "Response time < 200ms"
   ```

5. **Calculate Confidence Score**
   
   Based on:
   - Context completeness (2 points)
   - Pattern examples (2 points)  
   - Gotchas identified (2 points)
   - Test coverage (2 points)
   - Automation readiness (2 points)

## Output:

Save enhanced PRP to: `PRPs/active/$ARGUMENTS.md`

Link original PRD: `docs/prd/$ARGUMENTS.md`

## Example Usage:

```bash
# Convert existing PRD
/prd-to-prp user-authentication

# Convert with specific focus
/prd-to-prp payment-flow --focus security

# Convert and validate
/prd-to-prp data-pipeline && /prp-validate data-pipeline
```

## Integration:

After conversion:
1. Run `/prp-validate` to check completeness
2. Use `/gt --from-prp` to generate tasks
3. Enable `/prp-execute` for automation

The enhanced PRP maintains all original requirements while adding implementation intelligence for AI agents.