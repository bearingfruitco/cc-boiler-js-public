# Create Component with TDD - Enhanced

Create a new component with MANDATORY test-first development, design system validation, and optional ASCII wireframe step.

⚠️ **TDD IS NOW MANDATORY**: Tests will be generated BEFORE the component is created. Use `--no-tdd` flag to skip (not recommended).

## Usage
```bash
/create-component [type] [name] [options]
/cc [type] [name] [options]

# Options:
--wireframe    # Start with ASCII wireframe
--style=ref    # Use reference image for style
--animate      # Include animation planning
--no-tdd       # Skip test generation (NOT RECOMMENDED - requires confirmation)
```

## Enhanced TDD Flow

### Step 0: Test Generation (MANDATORY)

Before ANY component is created, comprehensive tests are generated:

```typescript
// UserProfile.test.tsx - Generated automatically
describe('UserProfile', () => {
  // Rendering tests
  it('renders user information correctly');
  it('displays placeholder when no image provided');
  
  // Props validation
  it('validates required props');
  it('handles optional props correctly');
  
  // Interaction tests
  it('calls onEdit when edit button clicked');
  it('shows loading state during updates');
  
  // Accessibility tests
  it('has proper ARIA labels');
  it('is keyboard navigable');
  
  // Design system compliance
  it('uses only approved font sizes');
  it('maintains 44px touch targets');
});
```

**This happens automatically!** The tdd-engineer agent will:
1. Analyze your component requirements
2. Check for existing PRPs/PRDs
3. Generate comprehensive test suite
4. Ensure all edge cases covered

### Step 1: ASCII Wireframe (Optional with --wireframe)

When using `--wireframe`, first generate a quick ASCII layout:

```
┌─────────────────────────────────┐
│ UserProfile Component           │
├─────────────────────────────────┤
│ ┌─────┐  Name: John Doe        │
│ │     │  Role: Developer        │
│ │ IMG │  ─────────────────      │
│ │     │  Bio text here...       │
│ └─────┘  spanning multiple      │
│          lines                  │
├─────────────────────────────────┤
│ [Edit Profile] [Settings]       │
└─────────────────────────────────┘
```

Benefits:
- Validate layout in 1 second
- Agree on structure before coding
- Show interactions (click → sidebar)

### Step 2: Apply Design System

After wireframe approval, generate with our strict rules:
- Font sizes: text-size-[1-4] only
- Font weights: font-regular, font-semibold only
- Spacing: 4px grid (p-1, p-2, p-3, etc.)
- Touch targets: minimum 44px (h-11)

### Step 3: Animation Planning (Optional with --animate)

Define micro-interactions:
```typescript
const animations = {
  hover: {
    trigger: "onMouseEnter",
    duration: "200ms",
    effect: "scale(1.02) + shadow-lg"
  },
  click: {
    trigger: "onClick", 
    duration: "150ms",
    effect: "scale(0.98)"
  }
};
```

### Step 4: Component Generation

Generate the actual component with all constraints applied.

**TDD Enforcement**: The component will ONLY be created after:
- ✅ Tests are written
- ✅ Tests are failing (RED phase)
- ✅ Ready for implementation (GREEN phase)

## Examples

### Basic Component (Now with TDD)
```bash
/cc ui Button

# Automatically:
# 1. Generates Button.test.tsx
# 2. Runs tests (fail)
# 3. Creates Button.tsx
# 4. Helps implement to pass tests
```

### With Wireframe First
```bash
/cc ui Card --wireframe

# Shows ASCII:
┌──────────────────┐
│ ┌────┐           │
│ │IMG │ Title     │
│ └────┘ Subtitle  │
│ Description...   │
│ [Action]         │
└──────────────────┘

# Then generates component
```

### With Animation Planning
```bash
/cc feature ProductCard --animate

# Plans animations:
- Hover: lift with shadow
- Image: lazy load fade-in
- Button: press effect
```

### Complete Flow (With Mandatory TDD)
```bash
/cc feature Dashboard --wireframe --animate

# 0. Generate Dashboard.test.tsx (AUTOMATIC)
# 1. ASCII wireframe
# 2. Confirm layout
# 3. Apply design system
# 4. Plan animations
# 5. Generate component
# 6. Verify all tests pass
```

### Skipping TDD (Not Recommended)
```bash
/cc ui QuickPrototype --no-tdd

# ⚠️  WARNING: Skipping TDD is not recommended!
# Confirm: Are you sure you want to create without tests? (y/N)
# Only proceed if absolutely necessary for prototypes
```

## Integration with Existing Commands

Works with:
- `/vd` - Validates generated component
- `/orch` - Can use frontend agent
- Design hooks - Still enforce rules

## Why TDD-First Works

1. **Quality Guarantee** - Every component has tests from day one
2. **Faster Development** - Tests guide implementation
3. **No Regressions** - Changes caught immediately
4. **Better Design** - TDD forces you to think about API first
5. **Automated** - No manual test writing needed

## TDD Workflow

```
/cc Button
   ↓
[Auto] Generate Button.test.tsx
   ↓
[Auto] Run tests (RED - failing)
   ↓
[User] Create Button.tsx
   ↓
[User] Implement until tests pass (GREEN)
   ↓
[Auto] Check coverage (must be >80%)
   ↓
[Optional] Refactor (tests still GREEN)
```

This ensures EVERY component follows TDD principles automatically!
