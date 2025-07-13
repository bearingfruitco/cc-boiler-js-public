#!/bin/bash

echo "🔧 Fixing dependencies and cleaning up..."

# Clean up existing installations
echo "📦 Cleaning node_modules and lock files..."
rm -rf node_modules
rm -rf pnpm-lock.yaml
rm -rf .pnpm-store

# Clear Next.js cache
echo "🗑️  Clearing Next.js cache..."
rm -rf .next
rm -rf .turbo

# Clear pnpm cache
echo "🧹 Clearing pnpm cache..."
pnpm store prune

# Install dependencies with exact versions
echo "📥 Installing dependencies..."
pnpm install --force

# Verify installations
echo ""
echo "✅ Verifying installations:"
echo "================================"
pnpm ls zod | grep -E "^zod|└─.*zod"
echo "--------------------------------"
pnpm ls drizzle-zod | grep -E "^drizzle-zod|└─.*drizzle-zod"
echo "--------------------------------"
pnpm ls @hookform/resolvers | grep -E "^@hookform/resolvers|└─.*@hookform/resolvers"
echo "--------------------------------"
pnpm ls tailwindcss | grep -E "^tailwindcss|└─.*tailwindcss"
echo "================================"

# Check for peer dependency issues
echo ""
echo "🔍 Checking for peer dependency issues..."
pnpm ls 2>&1 | grep -E "peer|unmet" || echo "✅ No peer dependency issues found!"

echo ""
echo "✨ Dependencies fixed! Now run:"
echo "  pnpm dev        # Start development server"
echo "  pnpm typecheck  # Check TypeScript issues"
