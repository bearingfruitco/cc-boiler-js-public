Capture a screenshot of the current component or page using the playwright-specialist agent.

Usage: /pw-screenshot [component-name] [options]

Options:
- full-page: Capture entire scrollable area
- mobile: Use mobile viewport
- dark-mode: Force dark theme

The agent will:
1. Navigate to the component/page
2. Wait for full render
3. Capture high-quality screenshot
4. Save with descriptive filename
5. Optionally annotate problem areas

Perfect for documentation, PR reviews, or visual debugging!