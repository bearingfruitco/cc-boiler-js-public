#!/bin/bash
# Quick setup script for new projects - one command to rule them all
# Usage: curl -sSL https://your-url/setup.sh | bash -s <project-name>

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BOILERPLATE_REPO="https://github.com/yourusername/claude-code-boilerplate.git"
BOILERPLATE_LOCAL="/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Get project name from argument
PROJECT_NAME=$1
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

echo "🚀 Setting up new Claude Code project: $PROJECT_NAME"
echo "================================================"

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check for required commands
for cmd in git node python3 gh; do
    if ! command -v $cmd &> /dev/null; then
        print_error "$cmd is not installed"
        exit 1
    fi
done
print_status "All required commands found"

# Check for pnpm (preferred) or npm
if command -v pnpm &> /dev/null; then
    PKG_MANAGER="pnpm"
elif command -v npm &> /dev/null; then
    PKG_MANAGER="npm"
    print_warning "pnpm not found, using npm (consider installing pnpm)"
else
    print_error "No package manager found (npm or pnpm)"
    exit 1
fi
print_status "Using $PKG_MANAGER"

# Create project directory
print_status "Creating project directory..."
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize git
print_status "Initializing git..."
git init --quiet

# Copy boilerplate
print_status "Copying boilerplate..."
if [ -d "$BOILERPLATE_LOCAL" ]; then
    # Use local copy if available
    cp -r "$BOILERPLATE_LOCAL/.claude" .
    cp "$BOILERPLATE_LOCAL/package.json" .
    cp "$BOILERPLATE_LOCAL/tailwind.config.js" .
    cp "$BOILERPLATE_LOCAL"/*.md .
    print_status "Used local boilerplate"
else
    # Clone from repo
    print_warning "Local boilerplate not found, cloning from repo..."
    git clone --quiet --depth 1 "$BOILERPLATE_REPO" .claude-temp
    cp -r .claude-temp/boilerplate/.claude .
    cp .claude-temp/boilerplate/package.json .
    cp .claude-temp/boilerplate/tailwind.config.js .
    cp .claude-temp/boilerplate/*.md .
    rm -rf .claude-temp
    print_status "Cloned from repository"
fi

# Create project structure
print_status "Creating project structure..."
mkdir -p app/{api,\(public\),\(protected\)} components/{ui,forms,layout,features} lib/{api,db,utils} hooks stores types docs

# Make scripts executable
print_status "Setting permissions..."
chmod +x .claude/scripts/*.sh
chmod +x .claude/scripts/*.py
chmod +x .claude/hooks/**/*.py 2>/dev/null || true

# Run hooks installer
print_status "Installing hooks..."
cd .claude/scripts

# Auto-answer the username prompt
if [ -n "${CLAUDE_USER:-}" ]; then
    echo "$CLAUDE_USER" | ./install-hooks.sh
else
    echo "shawn" | ./install-hooks.sh  # Default to shawn
fi

cd ../..

# Install dependencies
print_status "Installing dependencies..."
$PKG_MANAGER install --silent

# Create initial Next.js files
print_status "Creating initial files..."

# Create app/layout.tsx
cat > app/layout.tsx << 'EOF'
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Your App',
  description: 'Your app description',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
EOF

# Create app/globals.css
cat > app/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Create app/page.tsx
cat > app/page.tsx << 'EOF'
export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-md mx-auto p-4">
        <h1 className="text-size-1 font-semibold text-gray-900">
          Welcome to Your App
        </h1>
        <p className="text-size-3 font-regular text-gray-600 mt-4">
          Claude Code is ready. Run /help to see available commands.
        </p>
      </div>
    </div>
  );
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/

# Production
build/
dist/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Claude Code
.claude/team/registry.json
.claude/team/metrics/
.claude/team/logs/
.claude/team/handoffs/
.claude/team/debug/
EOF

# Update project-specific files
print_status "Customizing for $PROJECT_NAME..."
sed -i '' "s/Your App/$PROJECT_NAME/g" app/layout.tsx 2>/dev/null || sed -i "s/Your App/$PROJECT_NAME/g" app/layout.tsx
sed -i '' "s/your-app-name/$PROJECT_NAME/g" package.json 2>/dev/null || sed -i "s/your-app-name/$PROJECT_NAME/g" package.json

# Run health check
print_status "Running health check..."
python3 .claude/scripts/health-check.py || print_warning "Health check reported issues - see .claude/hooks/health-check-report.md"

# Initial commit
print_status "Creating initial commit..."
git add .
git commit -m "Initial setup with Claude Code boilerplate" --quiet

# Create GitHub repo (optional)
if [ "${CREATE_GITHUB_REPO:-false}" == "true" ]; then
    print_status "Creating GitHub repository..."
    gh repo create "$PROJECT_NAME" --private --source=. || print_warning "Could not create GitHub repo"
fi

# Success!
echo ""
echo "✅ Project setup complete!"
echo ""
echo "📁 Project location: $(pwd)"
echo ""
echo "🚀 Next steps:"
echo "   1. cd $PROJECT_NAME"
echo "   2. claude-code ."
echo "   3. Run /help to see all commands"
echo "   4. Update CLAUDE.md with project details"
echo ""
echo "👥 Team setup:"
echo "   - Current user: shawn"
echo "   - To change: echo '{\"current_user\": \"nikki\"}' > .claude/team/config.json"
echo ""
echo "🧪 Test your setup:"
echo "   - /cc ui Button    (create component)"
echo "   - /vd             (validate design)"
echo "   - /checkpoint     (save progress)"
echo ""
echo "Happy coding! 🎉"
