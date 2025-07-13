#!/bin/bash

echo "🔧 Fixing TypeScript file extensions..."

# Function to check if file contains JSX
contains_jsx() {
    local file=$1
    # Check for JSX syntax patterns
    if grep -E '<[A-Z][a-zA-Z]*[^>]*>|<\/[A-Z][a-zA-Z]*>|<[a-z]+[^>]*\/>|return\s*\(' "$file" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Fix component files
echo "📝 Checking component files..."
for file in components/**/*.ts; do
    if [[ -f "$file" ]] && contains_jsx "$file"; then
        new_file="${file%.ts}.tsx"
        echo "  ✏️  Renaming $file → $new_file"
        mv "$file" "$new_file"
    fi
done

# Fix lib files
echo "📝 Checking lib files..."
for file in lib/**/*.ts; do
    if [[ -f "$file" ]] && contains_jsx "$file"; then
        new_file="${file%.ts}.tsx"
        echo "  ✏️  Renaming $file → $new_file"
        mv "$file" "$new_file"
    fi
done

# Fix hooks files
echo "📝 Checking hooks files..."
for file in hooks/**/*.ts; do
    if [[ -f "$file" ]] && contains_jsx "$file"; then
        new_file="${file%.ts}.tsx"
        echo "  ✏️  Renaming $file → $new_file"
        mv "$file" "$new_file"
    fi
done

# Update imports in all TypeScript files
echo "🔄 Updating imports..."
find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | while read -r file; do
    # Update imports from .ts to .tsx where needed
    sed -i.bak -E "s/from '(.*)\/([^']+)\.ts'/from '\1\/\2'/g" "$file"
    sed -i.bak -E 's/from "(.*)\/([^"]+)\.ts"/from "\1\/\2"/g' "$file"
    rm -f "${file}.bak"
done

echo ""
echo "✅ File extensions fixed!"
echo ""
echo "🔍 Summary of changes:"
find . -name "*.tsx" -path "*/components/*" -o -path "*/hooks/*" -o -path "*/lib/*" | grep -v node_modules | wc -l | xargs echo "  - TSX files:"
find . -name "*.ts" -path "*/components/*" -o -path "*/hooks/*" -o -path "*/lib/*" | grep -v node_modules | grep -v "*.d.ts" | wc -l | xargs echo "  - TS files:"

echo ""
echo "💡 Next steps:"
echo "  1. Run: pnpm typecheck"
echo "  2. Fix any remaining import issues"
echo "  3. Commit the changes"
