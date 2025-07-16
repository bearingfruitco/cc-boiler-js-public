# Capture to Issue - Smart Issue Creation from Claude Responses

Captures Claude's response and intelligently creates or updates GitHub issues.

## Arguments:
- $TITLE: Title for the issue
- --section: Specific section to capture (e.g., "Implementation Plan")
- --check: Check for similar issues first (default: true)

## Usage Examples:

```bash
# Capture entire last response
/capture-to-issue "Implement caching strategy"

# Capture specific section
/capture-to-issue "Auth flow update" --section "Implementation Plan"

# Force new issue (skip similarity check)
/capture-to-issue "Bug fix" --check false
```

## Smart Duplicate Detection

The command will:

1. **Extract Key Concepts** from the captured content
2. **Search Existing Issues** for similar content
3. **Calculate Similarity Scores** using:
   - Title matching
   - Keyword overlap
   - PRD references
   - Component mentions

4. **Present Options** when similarities found:
   ```
   🔍 Found related issues:
   
   #23: "User Authentication System" (85% match)
        Status: Open, Assigned: @teammate
        
   #45: "Add OAuth Support" (40% match)
        Status: In Progress
   
   Options:
   1. Update issue #23 with new details
   2. Create sub-issue under #23
   3. Create new independent issue
   4. View issues and decide
   5. Cancel
   ```

## Integration with Existing Systems

### Issue Creation Flow:

```typescript
// 1. Get Claude's last response
const lastResponse = getClaudeContext();

// 2. Extract structured content
const content = {
  summary: extractSection(lastResponse, 'Summary'),
  plan: extractSection(lastResponse, 'Plan|Implementation'),
  tasks: extractTasks(lastResponse),
  components: extractComponentNames(lastResponse),
  dependencies: extractDependencies(lastResponse)
};

// 3. Search for related issues
const relatedIssues = await searchGitHubIssues({
  repo: getCurrentRepo(),
  keywords: content.keywords,
  state: 'open'
});

// 4. Calculate similarity
const similarities = relatedIssues.map(issue => ({
  ...issue,
  score: calculateSimilarity(content, issue)
}));

// 5. Present smart options
if (highSimilarityExists(similarities)) {
  // Suggest update or sub-issue
} else {
  // Create new with links to related
}
```

## Issue Body Template

```markdown
## 📋 Captured from Claude

$CAPTURED_CONTENT

## 🎯 Action Items
$EXTRACTED_TASKS

## 🔗 Context
- Session: $SESSION_ID
- Timestamp: $TIMESTAMP
- Branch: $CURRENT_BRANCH
- Related PRD: $PRD_REFERENCE
- Parent Issue: $PARENT_ISSUE (if applicable)

## 📦 Components Affected
$COMPONENT_LIST

## 🔄 Dependencies
- Uses: $DEPENDENCIES_IN
- Used by: $DEPENDENCIES_OUT

## 📊 Tracking
- Created by: /capture-to-issue
- Claude Context: $CONTEXT_HASH
```

## Prevents Common Problems:

1. **Duplicate Issues**: Smart detection before creation
2. **Lost Context**: Links to session and branch
3. **Orphaned Work**: Connects to PRDs and parent issues
4. **Missing Dependencies**: Auto-tracks component relationships

## Implementation Details:

### Similarity Calculation:
```python
def calculate_similarity(new_content, existing_issue):
    scores = {
        'title': fuzz.ratio(new_title, existing_issue.title) * 0.3,
        'keywords': keyword_overlap(new_content, existing_issue.body) * 0.4,
        'components': component_match(new_content, existing_issue) * 0.2,
        'prd_reference': prd_match(new_content, existing_issue) * 0.1
    }
    return sum(scores.values())
```

### Smart Merge Strategy:
- **> 80% match**: Suggest update existing
- **50-80% match**: Suggest sub-issue
- **< 50% match**: Create new with references

## Error Handling:

- No Claude context: "❌ No recent Claude response to capture"
- GitHub API fails: Falls back to manual issue creation
- No similar search: Creates issue with warning

## Configuration:

In `.claude/config.json`:
```json
{
  "capture_to_issue": {
    "similarity_threshold": 0.8,
    "check_by_default": true,
    "include_components": true,
    "include_dependencies": true,
    "max_content_length": 5000
  }
}
```

## Workflow Example:

```bash
# Claude provides plan
Claude: "Here's how we'll implement the caching system..."

# Capture it
/capture-to-issue "Implement caching"

> 🔍 Checking existing issues...
> Found: #34 "Add caching layer" (75% match)
> 
> This issue seems related. Would you like to:
> 1. Add your plan as a comment to #34
> 2. Create a sub-task for implementation
> 3. Create new issue (different approach)
> 
> Choose: 2

> ✅ Created issue #47 "Implement Redis caching"
> 🔗 Linked to parent #34
> 📦 Tracking components: CacheProvider, useCache
> 
> View: https://github.com/user/repo/issues/47
```
