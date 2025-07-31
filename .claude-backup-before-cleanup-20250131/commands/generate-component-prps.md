# Generate Component PRPs

Automatically generate Product Requirement Prompts (PRPs) for each major component identified in your architecture.

## Usage

```bash
/generate-component-prps [--from-architecture]
/gcp                     # alias
/component-prps          # alias
```

## Options

- `--from-architecture`: Parse architecture docs to identify components (default)
- `--interactive`: Ask for confirmation before generating each PRP
- `--priority`: Generate only high-priority components first

## What I'll Do

I'll analyze your architecture to identify major components and generate comprehensive PRPs for each. I'll use the specialized PRP writer agent to ensure high-quality, consistent PRPs:

```bash
# Use PRP writer agent for component PRPs
/spawn prp-writer "Generate PRPs for architecture components"
```

### Step 1: Component Analysis

I'll parse your architecture documents to identify:

1. **Frontend Components**
   - Page components (Dashboard, Forms, Analytics)
   - UI components (Header, Navigation, Cards)
   - Feature components (FormBuilder, DataVisualization)

2. **Backend Components**
   - API endpoints groups
   - Authentication system
   - Business logic services
   - Integration modules

3. **Infrastructure Components**
   - Database access layer
   - Caching system
   - Queue processors
   - File storage handlers

4. **Security Components**
   - Authentication flow
   - Authorization middleware
   - Audit logging system
   - Encryption services

### Step 2: Generate PRPs

For each identified component, I'll create a comprehensive PRP that includes:

```python
#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

class ComponentPRPGenerator:
    def __init__(self):
        self.arch_dir = Path("docs/architecture")
        self.prp_dir = Path("PRPs/active")
        self.template_dir = Path("PRPs/templates")
        self.components = []
        
    def analyze_and_generate(self, interactive=False, priority_only=False):
        """Main entry point"""
        print("🔍 Analyzing architecture for components...")
        
        # Ensure directories exist
        self.prp_dir.mkdir(parents=True, exist_ok=True)
        
        # Analyze architecture
        self.analyze_architecture()
        
        # Prioritize components
        self.prioritize_components()
        
        # Filter if needed
        if priority_only:
            self.components = [c for c in self.components if c["priority"] == "high"]
            
        print(f"\n📋 Found {len(self.components)} components to generate PRPs for:")
        for i, comp in enumerate(self.components, 1):
            print(f"{i}. {comp['name']} ({comp['category']}) - Priority: {comp['priority']}")
            
        if interactive:
            confirm = input("\nProceed with generation? (y/n): ")
            if confirm.lower() != 'y':
                print("Generation cancelled.")
                return
                
        # Generate PRPs
        generated = []
        for comp in self.components:
            prp_path = self.generate_component_prp(comp)
            if prp_path:
                generated.append(prp_path)
                print(f"✅ Generated: {prp_path}")
                
        # Create index
        self.create_prp_index(generated)
        
        print(f"\n🎉 Generated {len(generated)} component PRPs!")
        print(f"📁 Location: {self.prp_dir}/")
        print("\nNext steps:")
        print("1. Review generated PRPs for accuracy")
        print("2. Run `/prp-execute [component-name]` to validate")
        print("3. Start implementation with `/fw start [component]`")
        
    def analyze_architecture(self):
        """Parse all architecture documents"""
        components_found = []
        
        # System Design
        system_path = self.arch_dir / "SYSTEM_DESIGN.md"
        if system_path.exists():
            components_found.extend(self._parse_system_design(system_path))
            
        # Database Schema
        db_path = self.arch_dir / "DATABASE_SCHEMA.md"
        if db_path.exists():
            components_found.extend(self._parse_database_schema(db_path))
            
        # API Specification
        api_path = self.arch_dir / "API_SPECIFICATION.md"
        if api_path.exists():
            components_found.extend(self._parse_api_spec(api_path))
            
        # Frontend Architecture
        frontend_path = self.arch_dir / "FRONTEND_ARCHITECTURE.md"
        if frontend_path.exists():
            components_found.extend(self._parse_frontend_arch(frontend_path))
            
        # Security Design
        security_path = self.arch_dir / "SECURITY_DESIGN.md"
        if security_path.exists():
            components_found.extend(self._parse_security_design(security_path))
            
        # Deduplicate
        seen = set()
        for comp in components_found:
            key = comp["name"].lower()
            if key not in seen:
                seen.add(key)
                self.components.append(comp)
                
    def _parse_system_design(self, path: Path) -> List[Dict]:
        """Extract components from system design"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Look for component mentions
        sections = re.split(r'^#{1,3}\s+', content, flags=re.M)
        
        for section in sections:
            if 'Component' in section or 'Architecture' in section:
                # Frontend components
                if re.search(r'Dashboard|Analytics|Reporting', section, re.I):
                    components.append({
                        "name": "Analytics Dashboard",
                        "category": "frontend",
                        "priority": "high",
                        "dependencies": ["api", "charts"],
                        "description": "Real-time analytics and reporting dashboard"
                    })
                    
                if re.search(r'Form|Builder|Dynamic', section, re.I):
                    components.append({
                        "name": "Form Builder",
                        "category": "frontend",
                        "priority": "high",
                        "dependencies": ["api", "validation"],
                        "description": "Dynamic form creation and management system"
                    })
                    
                # Backend components
                if re.search(r'API|Gateway|REST', section, re.I):
                    components.append({
                        "name": "API Gateway",
                        "category": "backend",
                        "priority": "high",
                        "dependencies": ["auth", "database"],
                        "description": "RESTful API with authentication and rate limiting"
                    })
                    
                if re.search(r'Auth|Authentication|JWT', section, re.I):
                    components.append({
                        "name": "Authentication Service",
                        "category": "backend",
                        "priority": "critical",
                        "dependencies": ["database", "crypto"],
                        "description": "JWT-based authentication with OAuth support"
                    })
                    
        return components
        
    def _parse_database_schema(self, path: Path) -> List[Dict]:
        """Extract database-related components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Find main tables
        tables = re.findall(r'CREATE\s+TABLE\s+(?:public\.)?(\w+)', content, re.I)
        
        # Group related tables into modules
        if any(t in tables for t in ['users', 'accounts', 'profiles']):
            components.append({
                "name": "User Management",
                "category": "backend",
                "priority": "high",
                "dependencies": ["database", "auth"],
                "description": "User CRUD operations and profile management"
            })
            
        if any(t in tables for t in ['forms', 'form_fields', 'form_responses']):
            components.append({
                "name": "Form Data Service",
                "category": "backend",
                "priority": "high",
                "dependencies": ["database", "validation"],
                "description": "Form data storage and retrieval service"
            })
            
        return components
        
    def _parse_api_spec(self, path: Path) -> List[Dict]:
        """Extract API endpoint groups as components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Find endpoint groups
        endpoints = re.findall(r'(/api/v?\d*/(\w+))', content)
        groups = set(ep[1] for ep in endpoints)
        
        for group in groups:
            if group not in ['health', 'status']:  # Skip utility endpoints
                components.append({
                    "name": f"{group.title()} API",
                    "category": "backend",
                    "priority": "medium",
                    "dependencies": ["gateway", "database"],
                    "description": f"RESTful API endpoints for {group} operations"
                })
                
        return components
        
    def _parse_frontend_arch(self, path: Path) -> List[Dict]:
        """Extract frontend components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Component patterns
        if re.search(r'Header|Navigation|Layout', content, re.I):
            components.append({
                "name": "Layout System",
                "category": "frontend",
                "priority": "high",
                "dependencies": ["router", "auth"],
                "description": "Application layout with navigation and responsive design"
            })
            
        if re.search(r'Table|List|Grid', content, re.I):
            components.append({
                "name": "Data Display Components",
                "category": "frontend",
                "priority": "medium",
                "dependencies": ["api", "pagination"],
                "description": "Reusable data display components with sorting and filtering"
            })
            
        return components
        
    def _parse_security_design(self, path: Path) -> List[Dict]:
        """Extract security components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        if re.search(r'Audit|Log|Trail', content, re.I):
            components.append({
                "name": "Audit Logger",
                "category": "infrastructure",
                "priority": "high",
                "dependencies": ["database", "queue"],
                "description": "Comprehensive audit trail for all system actions"
            })
            
        if re.search(r'RBAC|Role|Permission', content, re.I):
            components.append({
                "name": "RBAC System",
                "category": "security",
                "priority": "critical",
                "dependencies": ["auth", "database"],
                "description": "Role-based access control with fine-grained permissions"
            })
            
        return components
        
    def prioritize_components(self):
        """Sort components by priority and dependencies"""
        # Priority order
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        
        # Sort by priority then by category
        self.components.sort(key=lambda x: (
            priority_order.get(x["priority"], 3),
            x["category"],
            x["name"]
        ))
        
    def generate_component_prp(self, component: Dict) -> str:
        """Generate PRP file for a component"""
        # Create filename
        filename = f"{component['name'].lower().replace(' ', '-')}-prp.md"
        filepath = self.prp_dir / filename
        
        # Load template if exists
        template_path = self.template_dir / "prp_typescript.md"
        if component["category"] == "frontend" and template_path.exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = self._get_default_template()
            
        # Generate content
        content = self._fill_template(template, component)
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(content)
            
        return filename
        
    def _get_default_template(self) -> str:
        """Default PRP template"""
        return '''# PRP: {name}

Generated: {timestamp}
Category: {category}
Priority: {priority}
Status: Ready for Implementation

## Overview

{description}

## Goals

### Primary Objectives
- Implement complete {name} functionality
- Ensure 100% test coverage
- Meet performance benchmarks
- Follow design system strictly

### Success Metrics
- All validation loops passing
- Zero accessibility violations
- Performance within targets
- Complete documentation

## Technical Context

### Architecture Integration
- Component Type: {category}
- Dependencies: {dependencies}
- Architecture Refs: See `docs/architecture/{category_upper}_*.md`

### Technology Stack
- Frontend: Next.js 15, React 19, TypeScript 5.3+
- Styling: Tailwind CSS (4 sizes, 2 weights, 4px grid)
- Backend: Supabase Edge Functions
- Database: PostgreSQL with RLS
- Testing: Vitest + Playwright

## Implementation Blueprint

### Phase 1: Foundation Setup
```bash
# Create component structure
/cc {component_name}

# Set up tests first (TDD)
/tdd {component_name}
```

Key tasks:
1. Define TypeScript interfaces
2. Create component skeleton
3. Write failing tests
4. Set up data models

### Phase 2: Core Implementation
```bash
# Implement with TDD workflow
/tdd-workflow {component_name}

# Validate continuously
/vd --watch
```

Key tasks:
1. Implement business logic
2. Build UI components
3. Add error handling
4. Create loading states

### Phase 3: Integration
```bash
# Test integration
/btf {component_name}

# Check async patterns
/validate-async
```

Key tasks:
1. Connect to APIs
2. Implement state management
3. Add real-time features
4. Handle edge cases

### Phase 4: Polish & Optimization
```bash
# Final validation
/prp-execute {component_name} --level 4

# Performance check
npm run lighthouse
```

Key tasks:
1. Performance optimization
2. Accessibility audit
3. Security review
4. Documentation

## Validation Loops

### Level 1: Continuous (Every Save)
```bash
npm run dev        # Hot reload
/vd               # Design validation
npm run typecheck # Type safety
```

### Level 2: Component Testing (After Each Feature)
```bash
npm test {component_name}
npm run test:components
```

### Level 3: Integration Testing (Phase Complete)
```bash
npm run test:e2e
/btf {component_name}
```

### Level 4: Production Readiness (Before PR)
```bash
/prp-execute {component_name} --all
npm run build
npm run analyze
```

## Critical Patterns

### Component Structure
```typescript
// Standard component pattern
export function {ComponentName}({{ 
  {destructured_props} 
}}: {ComponentName}Props) {{
  // 1. Hooks
  const {{ state, actions }} = use{ComponentName}();
  
  // 2. Effects
  useEffect(() => {{
    // Side effects
  }}, [dependencies]);
  
  // 3. Handlers
  const handleEvent = useCallback(() => {{
    // Event logic
  }}, [deps]);
  
  // 4. Render
  return (
    <div className="component-root">
      {{children}}
    </div>
  );
}}
```

### Design System Compliance
```css
/* ONLY use these font sizes */
.text-size-1 /* 32px - headings */
.text-size-2 /* 24px - subheadings */
.text-size-3 /* 16px - body text */
.text-size-4 /* 12px - captions */

/* ONLY use these weights */
.font-regular   /* 400 */
.font-semibold  /* 600 */

/* ONLY 4px grid spacing */
.p-1 .p-2 .p-3 .p-4 .p-6 .p-8
```

## Dependencies & Setup

### Required Packages
```json
{{
  "dependencies": {{
    // Component-specific deps
  }},
  "devDependencies": {{
    "@types/react": "^18.2.0",
    "vitest": "^1.0.0"
  }}
}}
```

### Environment Variables
```env
# Add to .env.local
{ENV_VARS}
```

## Known Gotchas & Solutions

### Common Issues
1. **Hydration Mismatch**: Use `useIsClient` hook
2. **Type Inference**: Explicitly type complex generics
3. **Bundle Size**: Dynamic import heavy dependencies
4. **Memory Leaks**: Clean up in useEffect returns

### Performance Targets
- First Load: < 3s
- Interaction: < 100ms
- Bundle Size: < 50KB
- Memory: < 50MB

## Acceptance Criteria

### Functional
- [ ] All features from architecture implemented
- [ ] Error states handled gracefully
- [ ] Loading states provide feedback
- [ ] Accessibility WCAG 2.1 AA compliant

### Technical
- [ ] TypeScript strict mode passing
- [ ] 90%+ test coverage
- [ ] No console errors/warnings
- [ ] Design system compliance 100%

### Documentation
- [ ] Component README created
- [ ] Storybook stories added
- [ ] API documentation complete
- [ ] Usage examples provided

## Resources

- Architecture: `/docs/architecture/`
- Design System: `/docs/design/design-system.md`
- Component Examples: `/components/examples/`
- Testing Guide: `/docs/testing/component-testing.md`

---

Ready to implement? Start with:
```bash
/fw start {component_name}
/spawn {specialist_agent}
```
'''
        
    def _fill_template(self, template: str, component: Dict) -> str:
        """Fill template with component data"""
        replacements = {
            "{name}": component["name"],
            "{timestamp}": datetime.now().isoformat(),
            "{category}": component["category"],
            "{category_upper}": component["category"].upper(),
            "{priority}": component["priority"],
            "{description}": component["description"],
            "{dependencies}": ", ".join(component["dependencies"]) if component["dependencies"] else "None",
            "{component_name}": component["name"].lower().replace(" ", "-"),
            "{ComponentName}": "".join(word.capitalize() for word in component["name"].split()),
            "{destructured_props}": "children, className, ...props",
            "{ENV_VARS}": f"NEXT_PUBLIC_{component['name'].upper().replace(' ', '_')}_ENABLED=true"
        }
        
        result = template
        for key, value in replacements.items():
            result = result.replace(key, value)
            
        return result
        
    def create_prp_index(self, generated_files: List[str]):
        """Create an index of generated PRPs"""
        index_path = self.prp_dir / "COMPONENT_PRPS.md"
        
        content = ["# Generated Component PRPs\n"]
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        content.append("## Components\n")
        
        for i, filename in enumerate(generated_files, 1):
            name = filename.replace("-prp.md", "").replace("-", " ").title()
            content.append(f"{i}. [{name}](./{filename})")
            
        content.append("\n## Usage\n")
        content.append("1. Review each PRP for accuracy")
        content.append("2. Run `/prp-execute [component-name]` to validate")
        content.append("3. Implement with `/fw start [component-name]`")
        content.append("4. Use `/spawn [agent]` for specialized help")
        
        with open(index_path, 'w') as f:
            f.write("\n".join(content))

# Execute the generator
if __name__ == "__main__":
    import sys
    
    interactive = "--interactive" in sys.argv
    priority_only = "--priority" in sys.argv
    
    generator = ComponentPRPGenerator()
    generator.analyze_and_generate(interactive=interactive, priority_only=priority_only)
```

### Step 3: Expected Output

After analyzing your architecture, I'll generate PRPs like:

```
🔍 Analyzing architecture for components...

📋 Found 8 components to generate PRPs for:
1. Authentication Service (backend) - Priority: critical
2. RBAC System (security) - Priority: critical
3. Analytics Dashboard (frontend) - Priority: high
4. Form Builder (frontend) - Priority: high
5. API Gateway (backend) - Priority: high
6. User Management (backend) - Priority: high
7. Audit Logger (infrastructure) - Priority: high
8. Data Display Components (frontend) - Priority: medium

✅ Generated: authentication-service-prp.md
✅ Generated: rbac-system-prp.md
✅ Generated: analytics-dashboard-prp.md
✅ Generated: form-builder-prp.md
✅ Generated: api-gateway-prp.md
✅ Generated: user-management-prp.md
✅ Generated: audit-logger-prp.md
✅ Generated: data-display-components-prp.md

🎉 Generated 8 component PRPs!
📁 Location: PRPs/active/

Next steps:
1. Review generated PRPs for accuracy
2. Run `/prp-execute [component-name]` to validate
3. Start implementation with `/fw start [component]`
```

## Integration with Architecture Workflow

This command integrates with:
- `/create-architecture` - Reads generated architecture docs
- `/validate-architecture` - Ensures architecture is complete first
- `/prp-execute` - Validates generated PRPs
- `/fw start` - Begins implementation of components
- `/spawn` - Gets specialized help for each component

## Benefits

1. **Consistency**: All components follow the same structure
2. **Completeness**: Nothing important is forgotten
3. **Efficiency**: No manual PRP creation needed
4. **Traceability**: Links back to architecture docs
5. **Quality**: Built-in validation loops

The generated PRPs ensure that every component is implemented with the same high standards and follows all architectural decisions!
