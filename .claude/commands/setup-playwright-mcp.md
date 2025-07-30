# Setup Playwright MCP Server

Automated setup for Playwright MCP integration with Claude Code.

## Usage
```bash
/setup-playwright-mcp [options]

Options:
  --wsl         Setup for WSL environment
  --docker      Setup with Docker support
  --headless    Configure for headless mode
```

## What it does:

### 1. Install Playwright MCP
```bash
# Add to Claude Code
claude mcp add playwright npx -y @mcp-get/playwright
```

### 2. Install Dependencies
```bash
# Install Playwright browsers
npx playwright install chromium

# For WSL - install additional dependencies
if [[ "$1" == "--wsl" ]]; then
  sudo apt-get update
  sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2
fi
```

### 3. Configure Environment
```javascript
// Create playwright config
const config = {
  use: {
    headless: options.headless ?? false,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
};
```

### 4. Create Test Structure
```bash
# Create directories
mkdir -p tests/e2e
mkdir -p tests/visual
mkdir -p tests/a11y
mkdir -p .claude/playwright

# Create example test
cat > tests/e2e/example.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Home/);
  
  // Check for console errors
  const logs = await page.evaluate(() => window.console.logs || []);
  expect(logs.filter(log => log.level === 'error')).toHaveLength(0);
});
EOF
```

### 5. Integration with Your System
```bash
# Add to package.json scripts
npm pkg set scripts.test:e2e="playwright test"
npm pkg set scripts.test:e2e:ui="playwright test --ui"
npm pkg set scripts.test:e2e:debug="playwright test --debug"

# Update your chains
echo "Browser testing ready! Use /pw commands"
```

### 6. Verify Installation
```bash
# Test Playwright MCP
/pw-verify Button

# Should launch browser and test
```

## Troubleshooting

### WSL Issues
```bash
# Display server needed
export DISPLAY=:0

# Or use xvfb
sudo apt-get install xvfb
xvfb-run -a npm run test:e2e
```

### Docker Issues
```bash
# Use playwright image
FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Or install deps
RUN npx playwright install-deps
```

### Permission Issues
```bash
# Fix permissions
chmod +x node_modules/.bin/playwright

# Clear cache
rm -rf ~/.cache/ms-playwright
```

## Quick Test

After setup, test with:
```bash
# Basic test
/pw "navigate to localhost:3000 and check if it loads"

# Component test
/pw-verify Button

# Form test
/pw-form ContactForm
```

## Environment Variables

Add to your .env:
```bash
# Playwright settings
PLAYWRIGHT_HEADLESS=false
PLAYWRIGHT_SLOW_MO=100
PLAYWRIGHT_TIMEOUT=30000
```

## Success Checklist
- [ ] Playwright MCP shows in Claude Code
- [ ] Browser launches with /pw commands
- [ ] No console errors on test pages
- [ ] Screenshots saved correctly
- [ ] WSL/Docker working (if applicable)

Setup complete! Start testing with `/pw` commands! 🎭
