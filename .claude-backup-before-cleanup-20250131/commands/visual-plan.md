# Visual Planning Mode

Enable Ray Fernando-style visual planning with screenshot analysis and iterative refinement.

## Usage
```bash
/visual-plan [description]
/vp [description]  # Short alias
```

## Features

### Screenshot Integration
1. Take screenshots of UI issues
2. Drag them into the planning interface
3. Claude analyzes visual elements
4. Compares against design system

### Iterative Planning
- Review proposed plans
- Respond with "keep planning" to refine
- Add constraints or requirements
- Ensure mobile/tablet considerations

## Workflow Example

```bash
# 1. Start visual planning
/vp "improve dashboard layout"

# 2. Drag screenshots into interface
# (Hold Shift while dragging in Cursor)

# 3. Describe the issue
"The dashboard feels cluttered on mobile.
Users can't find key actions easily."

# 4. Let Claude analyze with parallel agents
# - UI Analyst reviews layout
# - Pattern Researcher finds best practices  
# - Design System Checker ensures compliance

# 5. Review plan
# If not satisfied: "keep planning"
# If good: "proceed with implementation"
```

## Integration with UltraThink

Visual planning automatically triggers UltraThink when:
- Multiple screenshots provided
- Complex UI changes described
- Cross-platform considerations needed

```bash
# This automatically uses UltraThink
/vp "redesign responsive navigation" --screenshots 3
```

## Screenshot Analysis Features

- **Layout Issues**: Spacing, alignment, overflow
- **Responsive Problems**: Mobile/tablet specific issues
- **Design Violations**: Inconsistent with design system
- **Accessibility**: Color contrast, touch targets
- **Performance**: Identifies heavy components

## Planning Templates

### UI Improvement
```
Current State: [Screenshot analysis]
Problems Identified:
- Issue 1
- Issue 2
Proposed Solutions:
- Solution 1 (pros/cons)
- Solution 2 (pros/cons)
Recommendation: [Best approach]
```

### Bug Investigation  
```
Visual Evidence: [Screenshot analysis]
Expected vs Actual:
- Expected: [Description]
- Actual: [What's shown]
Potential Causes:
- Cause 1
- Cause 2
Investigation Plan:
1. Check [Component]
2. Verify [State]
3. Test [Scenario]
```

## Best Practices

1. **Multiple Angles**: Provide desktop and mobile screenshots
2. **Annotations**: Describe what's wrong in each screenshot
3. **Context**: Include relevant code files with screenshots
4. **Iterate**: Don't accept first plan, refine it
5. **Test Plan**: Ensure plan includes testing approach

## Related Commands
- `/ultra-think` - Deep analysis with parallel agents
- `/prd` - Formal requirements planning
- `/btf` - Browser test flows
- `/vd` - Validate design compliance
