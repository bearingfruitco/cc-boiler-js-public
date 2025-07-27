#!/bin/bash
# Test TDD Workflow - Demo Script

echo "🧪 TDD Workflow Demo"
echo "==================="
echo ""
echo "This demonstrates how the TDD hooks work in Claude Code."
echo ""

# Create a test directory
mkdir -p demo/components/__tests__

# Show what happens without tests
echo "1️⃣ Attempting to create component WITHOUT tests..."
echo ""
echo "In Claude Code, if you try:"
echo "  /cc UserProfile"
echo ""
echo "The TDD Enforcer will:"
echo "  ❌ Block the creation"
echo "  💡 Suggest writing tests first"
echo "  📝 Guide you to use /tdd-workflow"
echo ""

# Create a simple test file
echo "2️⃣ Creating test file first (TDD way)..."
cat > demo/components/__tests__/UserProfile.test.tsx << 'EOF'
import { render, screen } from '@testing-library/react';
import { UserProfile } from '../UserProfile';

describe('UserProfile', () => {
  it('should render user name', () => {
    render(<UserProfile name="John Doe" />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
EOF

echo "  ✅ Created: demo/components/__tests__/UserProfile.test.tsx"
echo ""

# Now create component
echo "3️⃣ Now creating component (tests exist)..."
cat > demo/components/UserProfile.tsx << 'EOF'
interface UserProfileProps {
  name: string;
}

export function UserProfile({ name }: UserProfileProps) {
  return (
    <div className="p-4 bg-white rounded-xl">
      <h2 className="text-size-2 font-semibold">{name}</h2>
    </div>
  );
}
EOF

echo "  ✅ Created: demo/components/UserProfile.tsx"
echo "  ✅ TDD Enforcer would ALLOW this (tests exist)"
echo ""

echo "4️⃣ Post-creation: Test Auto-Runner"
echo "  After saving the component, the Test Auto-Runner will:"
echo "  - Find UserProfile.test.tsx"
echo "  - Run tests automatically"
echo "  - Report results in Claude Code"
echo ""

echo "5️⃣ TDD Workflow Summary:"
echo "  🔴 RED: Write failing tests"
echo "  🟢 GREEN: Implement to pass tests"
echo "  ♻️  REFACTOR: Improve while tests stay green"
echo ""

echo "📚 Commands to try in Claude Code:"
echo "  /tdd-workflow contact-form    # Full TDD workflow"
echo "  /prd-generate-tests feature   # Generate from PRD"
echo "  /vd                          # Validate design"
echo ""

echo "🧹 Cleanup demo:"
echo "  rm -rf demo/"
echo ""

echo "✨ TDD Demo complete!"
