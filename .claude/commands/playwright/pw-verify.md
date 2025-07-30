Use the playwright-specialist agent to verify the current component or page renders correctly in a real browser.

If a component name is provided: /pw-verify Button
Otherwise, verify the most recently modified component.

The agent will:
1. Navigate to the component (in Storybook or dev server)
2. Check for console errors
3. Verify visual rendering
4. Test basic interactions
5. Validate design system compliance
6. Provide a browser test report

This catches issues that static analysis misses!