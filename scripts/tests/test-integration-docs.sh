#!/bin/bash

# Test script to verify integration documentation completeness

echo "=== Verifying Integration Documentation ==="
echo ""

# Check if all key files exist
MISSING_FILES=0

echo "Checking documentation files..."
for file in \
  "docs/setup/EXISTING_PROJECT_INTEGRATION.md" \
  "docs/setup/INTEGRATION_FILE_MANIFEST.md" \
  "scripts/integrate-boilerplate.sh" \
  "scripts/quick-add-boilerplate.sh" \
  "scripts/README.md"
do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ Missing: $file"
    ((MISSING_FILES++))
  fi
done

echo ""
echo "Checking if scripts are executable..."
for script in scripts/integrate-boilerplate.sh scripts/quick-add-boilerplate.sh; do
  if [ -x "$script" ]; then
    echo "✓ $script is executable"
  else
    echo "✗ $script is not executable"
    ((MISSING_FILES++))
  fi
done

echo ""
echo "Checking documentation references..."

# Check if EXISTING_PROJECT_INTEGRATION.md references the scripts
if grep -q "integrate-boilerplate.sh" docs/setup/EXISTING_PROJECT_INTEGRATION.md; then
  echo "✓ EXISTING_PROJECT_INTEGRATION.md references integration script"
else
  echo "✗ EXISTING_PROJECT_INTEGRATION.md missing script reference"
  ((MISSING_FILES++))
fi

# Check if it references the file manifest
if grep -q "INTEGRATION_FILE_MANIFEST.md" docs/setup/EXISTING_PROJECT_INTEGRATION.md; then
  echo "✓ EXISTING_PROJECT_INTEGRATION.md references file manifest"
else
  echo "✗ EXISTING_PROJECT_INTEGRATION.md missing manifest reference"
  ((MISSING_FILES++))
fi

# Check if README references the key docs
if grep -q "INTEGRATION_FILE_MANIFEST.md" docs/setup/README.md; then
  echo "✓ Setup README references file manifest"
else
  echo "✗ Setup README missing manifest reference"
  ((MISSING_FILES++))
fi

echo ""
echo "Checking script content..."

# Check if integration script handles all key directories
for dir in ".claude" ".agent-os" "PRPs" "field-registry" "components" "lib" "hooks" "stores"; do
  if grep -q "$dir" scripts/integrate-boilerplate.sh; then
    echo "✓ Integration script handles $dir"
  else
    echo "✗ Integration script missing $dir"
    ((MISSING_FILES++))
  fi
done

echo ""
echo "Checking for key config files..."
for config in "tailwind.config.js" "tsconfig.json" "drizzle.config.ts" "biome.json"; do
  if grep -q "$config" scripts/integrate-boilerplate.sh; then
    echo "✓ Integration script handles $config"
  else
    echo "✗ Integration script missing $config"
    ((MISSING_FILES++))
  fi
done

echo ""
echo "=== Summary ==="
if [ $MISSING_FILES -eq 0 ]; then
  echo "✅ All documentation and scripts are in place!"
  echo ""
  echo "Integration is ready to use:"
  echo "  curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate.sh | bash"
else
  echo "❌ Found $MISSING_FILES issues that need fixing"
fi
