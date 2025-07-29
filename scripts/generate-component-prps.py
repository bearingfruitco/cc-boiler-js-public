#!/usr/bin/env python3
"""
Component PRP Generator
Analyzes architecture documents and generates PRPs for identified components
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
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
            self.components = [c for c in self.components if c["priority"] in ["critical", "high"]]
            
        if not self.components:
            print("❌ No components found in architecture documents.")
            print("Make sure you have run /create-architecture first.")
            return
            
        print(f"\n📋 Found {len(self.components)} components to generate PRPs for:")
        for i, comp in enumerate(self.components, 1):
            icon = "🔴" if comp["priority"] == "critical" else "🟡" if comp["priority"] == "high" else "🟢"
            print(f"{i}. {icon} {comp['name']} ({comp['category']}) - Priority: {comp['priority']}")
            
        if interactive:
            confirm = input("\nProceed with generation? (y/n): ")
            if confirm.lower() != 'y':
                print("Generation cancelled.")
                return
                
        # Generate PRPs
        generated = []
        for comp in self.components:
            try:
                prp_path = self.generate_component_prp(comp)
                if prp_path:
                    generated.append(prp_path)
                    print(f"✅ Generated: {prp_path}")
            except Exception as e:
                print(f"❌ Failed to generate PRP for {comp['name']}: {str(e)}")
                
        # Create index
        if generated:
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
        
        # Check if architecture directory exists
        if not self.arch_dir.exists():
            print(f"❌ Architecture directory not found: {self.arch_dir}")
            print("Run /create-architecture first to generate architecture documents.")
            return
            
        # Parse each architecture document
        parsers = [
            ("SYSTEM_DESIGN.md", self._parse_system_design),
            ("DATABASE_SCHEMA.md", self._parse_database_schema),
            ("API_SPECIFICATION.md", self._parse_api_spec),
            ("FRONTEND_ARCHITECTURE.md", self._parse_frontend_arch),
            ("SECURITY_DESIGN.md", self._parse_security_design),
            ("TECHNICAL_ROADMAP.md", self._parse_roadmap)
        ]
        
        for filename, parser in parsers:
            path = self.arch_dir / filename
            if path.exists():
                try:
                    components = parser(path)
                    components_found.extend(components)
                    if components:
                        print(f"  ✓ Found {len(components)} components in {filename}")
                except Exception as e:
                    print(f"  ⚠️  Error parsing {filename}: {str(e)}")
                    
        # Deduplicate and clean
        seen = set()
        for comp in components_found:
            # Create unique key
            key = f"{comp['name'].lower()}_{comp['category']}"
            if key not in seen:
                seen.add(key)
                # Clean and validate component
                comp["name"] = comp["name"].strip()
                comp["dependencies"] = list(set(comp.get("dependencies", [])))
                comp["description"] = comp.get("description", "").strip()
                self.components.append(comp)
                
    def _parse_system_design(self, path: Path) -> List[Dict]:
        """Extract components from system design"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Look for component sections
        sections = re.split(r'^#{2,3}\s+', content, flags=re.M)
        
        for section in sections:
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            title = lines[0].strip()
            section_content = '\n'.join(lines[1:])
            
            # Frontend components
            if re.search(r'Frontend|Client|UI', title, re.I):
                if re.search(r'Dashboard|Analytics|Chart|Graph|Metric', section_content, re.I):
                    components.append({
                        "name": "Analytics Dashboard",
                        "category": "frontend",
                        "priority": "high",
                        "dependencies": ["api-client", "chart-library", "state-management"],
                        "description": "Interactive dashboard with real-time analytics and data visualization"
                    })
                    
                if re.search(r'Form|Input|Field|Builder', section_content, re.I):
                    components.append({
                        "name": "Dynamic Form Builder",
                        "category": "frontend",
                        "priority": "high",
                        "dependencies": ["validation-library", "ui-components", "api-client"],
                        "description": "Drag-and-drop form builder with conditional logic and validation"
                    })
                    
                if re.search(r'Navigation|Menu|Header|Layout', section_content, re.I):
                    components.append({
                        "name": "Layout System",
                        "category": "frontend",
                        "priority": "high",
                        "dependencies": ["router", "auth-hook", "ui-components"],
                        "description": "Responsive layout system with navigation and user context"
                    })
                    
            # Backend components
            elif re.search(r'Backend|Server|API|Service', title, re.I):
                if re.search(r'Auth|JWT|OAuth|Login', section_content, re.I):
                    components.append({
                        "name": "Authentication Service",
                        "category": "backend",
                        "priority": "critical",
                        "dependencies": ["jwt-library", "database", "encryption"],
                        "description": "Secure authentication with JWT tokens and OAuth2 integration"
                    })
                    
                if re.search(r'Gateway|Proxy|Route|Endpoint', section_content, re.I):
                    components.append({
                        "name": "API Gateway",
                        "category": "backend",
                        "priority": "high",
                        "dependencies": ["rate-limiter", "auth-middleware", "logger"],
                        "description": "Central API gateway with rate limiting and request routing"
                    })
                    
            # Infrastructure components
            elif re.search(r'Infrastructure|Deploy|Monitor', title, re.I):
                if re.search(r'Queue|Job|Task|Async', section_content, re.I):
                    components.append({
                        "name": "Job Queue System",
                        "category": "infrastructure",
                        "priority": "medium",
                        "dependencies": ["queue-library", "worker-pool", "monitoring"],
                        "description": "Asynchronous job processing with retry logic and monitoring"
                    })
                    
        return components
        
    def _parse_database_schema(self, path: Path) -> List[Dict]:
        """Extract database-related components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Find CREATE TABLE statements
        tables = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:public\.)?(\w+)', content, re.I)
        
        # Group related tables into logical components
        table_groups = {
            "user": ["users", "profiles", "accounts", "sessions"],
            "form": ["forms", "form_fields", "form_responses", "form_templates"],
            "analytics": ["analytics", "events", "metrics", "reports"],
            "audit": ["audit_log", "activity_log", "changes", "history"]
        }
        
        for group_name, group_tables in table_groups.items():
            if any(table.lower() in group_tables for table in tables):
                if group_name == "user":
                    components.append({
                        "name": "User Management Module",
                        "category": "backend",
                        "priority": "high",
                        "dependencies": ["database", "auth-service", "validation"],
                        "description": "Complete user lifecycle management with profiles and preferences"
                    })
                elif group_name == "form":
                    components.append({
                        "name": "Form Data Service",
                        "category": "backend",
                        "priority": "high",
                        "dependencies": ["database", "validation", "storage"],
                        "description": "Form data persistence with versioning and response handling"
                    })
                elif group_name == "analytics":
                    components.append({
                        "name": "Analytics Engine",
                        "category": "backend",
                        "priority": "medium",
                        "dependencies": ["database", "queue", "aggregation"],
                        "description": "Real-time analytics processing and aggregation service"
                    })
                elif group_name == "audit":
                    components.append({
                        "name": "Audit Logger",
                        "category": "infrastructure",
                        "priority": "high",
                        "dependencies": ["database", "queue", "encryption"],
                        "description": "Comprehensive audit trail with tamper-proof logging"
                    })
                    
        return components
        
    def _parse_api_spec(self, path: Path) -> List[Dict]:
        """Extract API endpoint groups as components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Find API endpoint patterns
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/api/v?\d*/(\w+))'
        endpoints = re.findall(endpoint_pattern, content, re.I)
        
        # Group endpoints by resource
        resource_groups = {}
        for method, full_path, resource in endpoints:
            if resource not in resource_groups:
                resource_groups[resource] = []
            resource_groups[resource].append(method.upper())
            
        # Create components for significant resources
        for resource, methods in resource_groups.items():
            if resource in ['health', 'status', 'ping']:  # Skip utility endpoints
                continue
                
            # Determine if it's a full CRUD resource
            has_crud = all(m in methods for m in ['GET', 'POST', 'PUT', 'DELETE'])
            
            components.append({
                "name": f"{resource.title()} API Service",
                "category": "backend",
                "priority": "high" if has_crud else "medium",
                "dependencies": ["api-gateway", "database", "validation"],
                "description": f"RESTful API service for {resource} with {', '.join(set(methods))} operations"
            })
            
        return components
        
    def _parse_frontend_arch(self, path: Path) -> List[Dict]:
        """Extract frontend components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Look for component definitions
        comp_patterns = [
            (r'Table|DataGrid|List.*Component', "Data Display Components", 
             "Reusable components for displaying tabular and list data with sorting/filtering"),
            (r'Modal|Dialog|Popup|Overlay', "Modal System", 
             "Centralized modal management with animations and backdrop"),
            (r'Notification|Toast|Alert|Banner', "Notification System", 
             "User feedback system with toast notifications and alerts"),
            (r'Search|Filter|Query', "Search Interface", 
             "Advanced search with filters and saved queries"),
            (r'Upload|File|Attachment', "File Upload System", 
             "Drag-and-drop file upload with progress tracking")
        ]
        
        for pattern, name, description in comp_patterns:
            if re.search(pattern, content, re.I):
                components.append({
                    "name": name,
                    "category": "frontend",
                    "priority": "medium",
                    "dependencies": ["ui-library", "state-management", "api-client"],
                    "description": description
                })
                
        return components
        
    def _parse_security_design(self, path: Path) -> List[Dict]:
        """Extract security components"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Security components
        security_patterns = [
            (r'RBAC|Role.?Based|Permission|Access.?Control', "RBAC Authorization System", 
             "critical", "Fine-grained role-based access control with dynamic permissions"),
            (r'Encrypt|Crypto|Key.?Management', "Encryption Service", 
             "high", "Field-level encryption with key rotation and secure storage"),
            (r'Rate.?Limit|Throttl|DDoS|Brute.?Force', "Rate Limiter", 
             "high", "Intelligent rate limiting with sliding windows and IP tracking"),
            (r'CSRF|XSS|Injection|Vulnerability', "Security Middleware", 
             "critical", "Comprehensive security middleware for common attack vectors"),
            (r'2FA|Two.?Factor|MFA|Multi.?Factor', "Multi-Factor Auth", 
             "high", "TOTP-based 2FA with backup codes and device management")
        ]
        
        for pattern, name, priority, description in security_patterns:
            if re.search(pattern, content, re.I):
                components.append({
                    "name": name,
                    "category": "security",
                    "priority": priority,
                    "dependencies": ["auth-service", "database", "cache"],
                    "description": description
                })
                
        return components
        
    def _parse_roadmap(self, path: Path) -> List[Dict]:
        """Extract components from technical roadmap"""
        components = []
        with open(path, 'r') as f:
            content = f.read()
            
        # Look for phase definitions
        phase_pattern = r'Phase\s+\d+[:\s-]+([^\n]+)'
        phases = re.findall(phase_pattern, content, re.I)
        
        # Extract components mentioned in early phases
        for phase in phases[:2]:  # Focus on first two phases
            if re.search(r'Monitor|Observ|Metric|Log', phase, re.I):
                components.append({
                    "name": "Monitoring Dashboard",
                    "category": "infrastructure",
                    "priority": "medium",
                    "dependencies": ["metrics-library", "api-client", "charts"],
                    "description": "Real-time system monitoring with alerts and metrics"
                })
                
            if re.search(r'CI/CD|Deploy|Pipeline|Automat', phase, re.I):
                components.append({
                    "name": "Deployment Pipeline",
                    "category": "infrastructure",
                    "priority": "medium",
                    "dependencies": ["ci-tools", "testing", "monitoring"],
                    "description": "Automated deployment pipeline with rollback capabilities"
                })
                
        return components
        
    def prioritize_components(self):
        """Sort components by priority and dependencies"""
        # Define priority order
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        category_order = {"security": 0, "backend": 1, "frontend": 2, "infrastructure": 3}
        
        # Sort by priority, then category, then name
        self.components.sort(key=lambda x: (
            priority_order.get(x["priority"], 3),
            category_order.get(x["category"], 3),
            x["name"]
        ))
        
    def generate_component_prp(self, component: Dict) -> str:
        """Generate PRP file for a component"""
        # Create safe filename
        safe_name = re.sub(r'[^\w\s-]', '', component["name"].lower())
        safe_name = re.sub(r'[-\s]+', '-', safe_name)
        filename = f"{safe_name}-prp.md"
        filepath = self.prp_dir / filename
        
        # Check if file already exists
        if filepath.exists():
            print(f"  ⚠️  Skipping {filename} (already exists)")
            return None
            
        # Generate content using the template approach
        # In a real implementation, this would call the PRP writer agent
        content = self._generate_prp_content(component)
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(content)
            
        # Update PRP tracking files
        self._update_prp_tracking(component, filename)
            
        return filename
        
    def _update_prp_tracking(self, component: Dict, filename: str):
        """Update PRP tracking files for integration"""
        # Update active PRPs list
        active_prps_file = self.prp_dir.parent / "active_prps.json"
        if active_prps_file.exists():
            with open(active_prps_file, 'r') as f:
                active_prps = json.load(f)
        else:
            active_prps = {}
            
        # Add new PRP
        prp_id = filename.replace('-prp.md', '')
        active_prps[prp_id] = {
            "name": component["name"],
            "filename": filename,
            "category": component["category"],
            "priority": component["priority"],
            "status": "ready",
            "created": datetime.now().isoformat(),
            "source": "architecture"
        }
        
        # Write updated tracking
        with open(active_prps_file, 'w') as f:
            json.dump(active_prps, f, indent=2)
        
    def _generate_prp_content(self, component: Dict) -> str:
        """Generate PRP content for a component"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safe_name = component["name"].replace(" ", "").replace("-", "")
        component_var = component["name"].lower().replace(" ", "-").replace("_", "-")
        
        # Determine test commands based on category
        test_commands = {
            "frontend": f"npm test components/{component_var}",
            "backend": f"npm test services/{component_var}",
            "infrastructure": f"npm test infra/{component_var}",
            "security": f"npm test security/{component_var}"
        }.get(component["category"], "npm test")
        
        return f"""# PRP: {component['name']}

Generated: {timestamp}
Category: {component['category']}
Priority: {component['priority']}
Status: Ready for Implementation

## Overview

{component['description']}

This component is a critical part of the {component['category']} layer and must integrate seamlessly with the overall system architecture while maintaining strict compliance with our design system and security standards.

## Goals

### Primary Objectives
1. Implement complete {component['name']} functionality as specified in architecture
2. Achieve 100% test coverage with comprehensive edge case handling
3. Meet or exceed performance benchmarks (response time < 200ms)
4. Ensure strict design system compliance (4 sizes, 2 weights, 4px grid)
5. Implement comprehensive security controls and audit logging

### Success Metrics
- All 4 validation levels passing (syntax → component → integration → production)
- Zero accessibility violations (WCAG 2.1 AA compliant)
- Performance metrics within targets (Core Web Vitals)
- Complete API documentation with examples
- Security audit passed with no critical issues

## Technical Context

### Architecture Integration
- **Component Category**: {component['category']}
- **Dependencies**: {', '.join(component['dependencies']) if component['dependencies'] else 'None'}
- **Architecture References**: 
  - System Design: `docs/architecture/SYSTEM_DESIGN.md`
  - Specific Design: `docs/architecture/{component['category'].upper()}_ARCHITECTURE.md`
  - Security Requirements: `docs/architecture/SECURITY_DESIGN.md`

### Technology Stack
- **Frontend**: Next.js 15, React 19, TypeScript 5.3+, Tailwind CSS
- **Backend**: Supabase Edge Functions, PostgreSQL 15+
- **Testing**: Vitest for unit tests, Playwright for E2E
- **Monitoring**: Sentry for errors, custom metrics for performance
- **Security**: Row Level Security, JWT authentication, field encryption

## Implementation Blueprint

### Phase 1: Foundation Setup (Day 1)

#### 1.1 Component Structure
```bash
# Create component structure with TDD
/tdd {component_var}

# For frontend components
/cc {component_var} --type={component['category']}

# Set up test environment
npm run test:watch {component_var}
```

#### 1.2 Type Definitions
```typescript
// Define all interfaces upfront
interface {safe_name}Props {{
  // Component props
}}

interface {safe_name}State {{
  // State shape
}}

interface {safe_name}Context {{
  // Context if needed
}}

type {safe_name}Action = 
  | {{ type: 'INIT'; payload: InitData }}
  | {{ type: 'UPDATE'; payload: UpdateData }}
  | {{ type: 'ERROR'; payload: Error }};
```

#### 1.3 Initial Tests (TDD)
```typescript
describe('{component['name']}', () => {{
  it('should initialize correctly', () => {{
    // Test initialization
  }});
  
  it('should handle primary use case', () => {{
    // Test main functionality
  }});
  
  it('should handle error states', () => {{
    // Test error handling
  }});
}});
```

### Phase 2: Core Implementation (Day 2-3)

#### 2.1 Business Logic
```typescript
// Implement core functionality
export function use{safe_name}() {{
  const [state, dispatch] = useReducer(reducer, initialState);
  
  // Core logic here
  
  return {{
    state,
    actions: {{
      // Exposed actions
    }}
  }};
}}
```

#### 2.2 Component Implementation
```typescript
export function {safe_name}({{
  children,
  className,
  ...props
}}: {safe_name}Props) {{
  // 1. Hooks (always first)
  const {{ state, actions }} = use{safe_name}();
  const {{ user }} = useAuth();
  
  // 2. Effects
  useEffect(() => {{
    // Initialization
    return () => {{
      // Cleanup
    }};
  }}, []);
  
  // 3. Event Handlers
  const handleAction = useCallback(async (data: ActionData) => {{
    try {{
      setLoading(true);
      await actions.performAction(data);
      toast.success('Action completed');
    }} catch (error) {{
      toast.error('Action failed');
      console.error('Error in {component_var}:', error);
    }} finally {{
      setLoading(false);
    }}
  }}, [actions]);
  
  // 4. Render
  return (
    <div className={`
      {component_var}-container
      space-y-4  /* 4px grid */
      p-4        /* 16px padding */
      ${{className}}
    `}}>
      {{/* Component content */}}
    </div>
  );
}}
```

#### 2.3 API Integration (if backend)
```typescript
// API endpoint implementation
export async function handle{safe_name}Request(req: Request) {{
  // 1. Authentication
  const {{ user }} = await authenticateRequest(req);
  if (!user) return unauthorized();
  
  // 2. Validation
  const {{ data, error }} = await validateInput(req);
  if (error) return badRequest(error);
  
  // 3. Authorization
  const canAccess = await authorize(user, data);
  if (!canAccess) return forbidden();
  
  // 4. Business Logic
  try {{
    const result = await process{safe_name}(data);
    
    // 5. Audit Log
    await auditLog({{
      user: user.id,
      action: '{component_var}.process',
      resource: result.id,
      metadata: {{ ...data }}
    }});
    
    return json(result);
  }} catch (error) {{
    return serverError(error);
  }}
}}
```

### Phase 3: Integration & Polish (Day 4-5)

#### 3.1 Integration Tests
```bash
# Run integration tests
/btf {component_var}

# Check async patterns
/validate-async

# Performance testing
npm run perf:test {component_var}
```

#### 3.2 Accessibility Audit
```typescript
// Ensure WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support  
- Color contrast (4.5:1 minimum)
- Focus indicators
- ARIA labels
```

#### 3.3 Performance Optimization
```typescript
// Optimization checklist
- [ ] Code splitting implemented
- [ ] Images optimized (next/image)
- [ ] Memoization for expensive operations
- [ ] Debounced API calls
- [ ] Virtual scrolling for large lists
```

#### 3.4 Documentation
```markdown
# {component['name']} Documentation

## Overview
[Component description]

## Usage
```tsx
import {{ {safe_name} }} from '@/components/{component_var}';

function Example() {{
  return (
    <{safe_name}
      prop1="value"
      onAction={{handleAction}}
    />
  );
}}
```

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| ... | ... | ... | ... |

## Examples
[Multiple usage examples]
```

## Validation Loops

### 🔴 Level 1: Code Quality (Every Save)
```bash
# Continuous validation
/vd                          # Design system check
npm run lint                 # Linting
npm run typecheck            # TypeScript
```

Requirements:
- ✅ Design tokens only (text-size-[1-4], font-regular/semibold)
- ✅ 4px spacing grid (p-1, p-2, p-3, p-4, p-6, p-8)
- ✅ No TypeScript errors
- ✅ No console.logs in production code

### 🟡 Level 2: Component Testing (After Basic Implementation)
```bash
# Component testing
{test_commands}
npm run test:components
```

Requirements:
- ✅ 100% code coverage
- ✅ All edge cases tested
- ✅ Error states handled
- ✅ Loading states implemented

### 🟢 Level 3: Integration Testing (After Features Complete)
```bash
# Integration testing
npm run test:e2e:{component_var}
/btf {component_var}
```

Requirements:
- ✅ End-to-end flows working
- ✅ API integration tested
- ✅ Real database queries tested
- ✅ Error recovery verified

### 🔵 Level 4: Production Readiness (Before PR)
```bash
# Final validation
/prp-execute {component_var} --level 4
npm run build
npm run analyze
```

Requirements:
- ✅ Bundle size < 50KB
- ✅ Lighthouse score > 90
- ✅ No security vulnerabilities
- ✅ Documentation complete

## Critical Patterns & Anti-Patterns

### ✅ DO: Follow These Patterns

#### Component Structure
```typescript
// Consistent component structure
const {safe_name}: FC<{safe_name}Props> = ({{ ...props }}) => {{
  // 1. Hooks at top
  // 2. Effects next
  // 3. Handlers
  // 4. Early returns
  // 5. Main render
}};
```

#### Error Handling
```typescript
// Comprehensive error handling
try {{
  setLoading(true);
  const result = await riskyOperation();
  setData(result);
}} catch (error) {{
  setError(error);
  toast.error(getErrorMessage(error));
  logError(error, {{ component: '{component_var}' }});
}} finally {{
  setLoading(false);
}}
```

#### Design System Usage
```tsx
// Correct design system usage
<h2 className="text-size-2 font-semibold text-gray-900">
  Heading
</h2>
<p className="text-size-3 font-regular text-gray-600 mt-2">
  Body text with proper spacing
</p>
<button className="h-12 px-4 text-size-3 font-semibold bg-blue-600 text-white rounded-xl">
  Action Button
</button>
```

### ❌ AVOID: Common Anti-Patterns

1. **Direct DOM Manipulation** - Use React state
2. **Inline Styles** - Use Tailwind classes
3. **Any Type** - Always define proper types
4. **Synchronous Blocking** - Use async/await
5. **Hardcoded Values** - Use constants/env vars

## Performance Requirements

### Target Metrics
- **First Load**: < 3s (mobile 4G)
- **Interaction**: < 100ms response
- **Bundle Size**: < 50KB (gzipped)
- **Memory**: < 50MB heap size
- **API Response**: < 200ms p95

### Optimization Strategies
1. Use React.memo for expensive components
2. Implement virtual scrolling for lists > 100 items
3. Lazy load non-critical components
4. Optimize images with next/image
5. Use Web Workers for heavy computations

## Security Checklist

- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] CSRF tokens for state-changing operations
- [ ] Rate limiting on API endpoints
- [ ] Audit logging for sensitive operations
- [ ] PII data encrypted at rest
- [ ] RLS policies for data access
- [ ] Security headers configured

## Dependencies & Environment

### NPM Dependencies
```json
{{
  "dependencies": {{
    // Component-specific dependencies
    {self._get_dependencies_json(component)}
  }},
  "devDependencies": {{
    "@types/react": "^18.2.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0"
  }}
}}
```

### Environment Variables
```env
# Add to .env.local
NEXT_PUBLIC_{component_var.upper().replace('-', '_')}_ENABLED=true
NEXT_PUBLIC_{component_var.upper().replace('-', '_')}_API_URL=/api/{component_var}
{component_var.upper().replace('-', '_')}_SECRET_KEY={{generate-secret-key}}
```

## Common Issues & Solutions

### Issue 1: Hydration Mismatch
**Problem**: Server and client render differently
**Solution**: Use `useIsClient()` hook for client-only features
```typescript
const isClient = useIsClient();
if (!isClient) return <Skeleton />;
```

### Issue 2: Race Conditions
**Problem**: Multiple concurrent API calls
**Solution**: Use AbortController
```typescript
useEffect(() => {{
  const controller = new AbortController();
  fetchData({{ signal: controller.signal }});
  return () => controller.abort();
}}, []);
```

### Issue 3: Memory Leaks
**Problem**: Subscriptions not cleaned up
**Solution**: Always return cleanup function
```typescript
useEffect(() => {{
  const subscription = subscribe();
  return () => subscription.unsubscribe();
}}, []);
```

## Acceptance Criteria

### Functional Requirements
- [ ] All features from architecture document implemented
- [ ] Handles all specified use cases
- [ ] Error states provide clear user feedback
- [ ] Loading states prevent user confusion
- [ ] Works across all supported browsers

### Technical Requirements
- [ ] TypeScript strict mode passing
- [ ] 90%+ test coverage (target 100%)
- [ ] No console errors or warnings
- [ ] Passes all 4 validation levels
- [ ] Meets performance benchmarks

### Documentation Requirements
- [ ] Component README with examples
- [ ] API documentation (if applicable)
- [ ] Storybook stories created
- [ ] Architecture decision records updated
- [ ] Runbook for common issues

### Security Requirements
- [ ] Security audit passed
- [ ] No known vulnerabilities
- [ ] PII handling compliant
- [ ] Authentication/authorization working
- [ ] Audit logging implemented

## Resources & References

### Internal Resources
- Architecture: `/docs/architecture/`
- Design System: `/docs/design/design-system.md`
- Security Guide: `/docs/SECURITY_GUIDE.md`
- Testing Guide: `/docs/testing/`

### External Resources
- [React Best Practices](https://react.dev/learn)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [OWASP Security Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Component Examples
- Similar Component: `/components/{self._find_similar_component(component)}`
- Design Patterns: `/components/examples/`
- Test Examples: `/tests/components/`

## Getting Started

Ready to implement {component['name']}? Start here:

```bash
# 1. Set up your environment
/sr                              # Smart resume
/cp load {component['category']} # Load appropriate context

# 2. Start implementation
/fw start {component_var}        # Begin feature workflow
/spawn {self._get_specialist_agent(component)}  # Get specialized help

# 3. Follow TDD workflow
/tdd {component_var}             # Test-driven development

# 4. Validate continuously
/prp-execute {component_var}     # Run validation loops
```

Remember: This PRP is your single source of truth. Follow it closely for implementation success!

---
Generated by Component PRP Generator
Architecture-Driven Development™️
"""

    def _get_dependencies_json(self, component: Dict) -> str:
        """Get dependency JSON based on component type"""
        deps = {}
        
        # Common dependencies
        if "validation" in component.get("dependencies", []):
            deps["zod"] = "^3.22.0"
            deps["react-hook-form"] = "^7.48.0"
            
        if "chart" in component.get("dependencies", []) or "analytics" in component["name"].lower():
            deps["recharts"] = "^2.10.0"
            deps["d3"] = "^7.8.0"
            
        if "auth" in component.get("dependencies", []):
            deps["jsonwebtoken"] = "^9.0.0"
            
        if "queue" in component.get("dependencies", []):
            deps["bullmq"] = "^5.0.0"
            
        # Format as JSON
        if deps:
            return '\n    '.join(f'"{k}": "{v}",' for k, v in deps.items()).rstrip(',')
        return '// No additional dependencies required'
        
    def _find_similar_component(self, component: Dict) -> str:
        """Find a similar existing component"""
        similar = {
            "frontend": "ui/Card",
            "backend": "api/users",
            "infrastructure": "workers/queue-processor",
            "security": "middleware/auth"
        }
        return similar.get(component["category"], "ui/Button")
        
    def _get_specialist_agent(self, component: Dict) -> str:
        """Get the right specialist agent for the component"""
        specialists = {
            "frontend": "frontend-ux-specialist",
            "backend": "backend-reliability-engineer", 
            "infrastructure": "platform-deployment",
            "security": "security-threat-analyst"
        }
        return specialists.get(component["category"], "senior-engineer")
        
    def create_prp_index(self, generated_files: List[str]):
        """Create an index of generated PRPs"""
        index_path = self.prp_dir / "COMPONENT_PRPS_INDEX.md"
        
        content = [
            "# Component PRPs Index",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Components: {len(generated_files)}",
            "\n## Components by Priority\n"
        ]
        
        # Group by priority
        by_priority = {"critical": [], "high": [], "medium": [], "low": []}
        
        for filename in generated_files:
            # Find matching component
            for comp in self.components:
                comp_filename = f"{comp['name'].lower().replace(' ', '-').replace('_', '-')}-prp.md"
                if comp_filename == filename:
                    by_priority[comp["priority"]].append((filename, comp))
                    break
                    
        # Add to index
        for priority in ["critical", "high", "medium", "low"]:
            if by_priority[priority]:
                icon = "🔴" if priority == "critical" else "🟡" if priority == "high" else "🟢"
                content.append(f"\n### {icon} {priority.title()} Priority\n")
                for filename, comp in by_priority[priority]:
                    content.append(f"1. **[{comp['name']}](./{filename})**")
                    content.append(f"   - Category: {comp['category']}")
                    content.append(f"   - {comp['description']}")
                    
        # Add usage instructions
        content.extend([
            "\n## Implementation Guide\n",
            "### 1. Choose a Component",
            "Start with critical/high priority components that have few dependencies.\n",
            "### 2. Review the PRP",
            "```bash",
            "cat PRPs/active/[component-name]-prp.md",
            "```\n",
            "### 3. Validate Environment",
            "```bash", 
            "/prp-execute [component-name] --level 1",
            "```\n",
            "### 4. Start Implementation",
            "```bash",
            "/fw start [component-name]",
            "/spawn [specialist-agent]  # Get expert help",
            "```\n",
            "### 5. Follow TDD Workflow",
            "```bash",
            "/tdd [component-name]",
            "```\n",
            "### 6. Validate Each Phase",
            "Run validation after each implementation phase:",
            "- Level 1: After setup (syntax/linting)",
            "- Level 2: After basic implementation (component tests)",
            "- Level 3: After integration (e2e tests)",
            "- Level 4: Before PR (production readiness)\n",
            "### 7. Complete Implementation",
            "```bash",
            "/fw complete [component-name]",
            "```"
        ])
        
        with open(index_path, 'w') as f:
            f.write("\n".join(content))
            
        print(f"\n📇 Created index: {index_path}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PRPs for architecture components")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Ask for confirmation before generating")
    parser.add_argument("--priority", "-p", action="store_true",
                       help="Only generate high/critical priority components")
    parser.add_argument("--arch-dir", default="docs/architecture",
                       help="Architecture directory path")
    parser.add_argument("--prp-dir", default="PRPs/active",
                       help="PRP output directory")
    
    args = parser.parse_args()
    
    # Create generator with custom paths if provided
    generator = ComponentPRPGenerator()
    if args.arch_dir:
        generator.arch_dir = Path(args.arch_dir)
    if args.prp_dir:
        generator.prp_dir = Path(args.prp_dir)
        
    # Run generation
    generator.analyze_and_generate(
        interactive=args.interactive,
        priority_only=args.priority
    )


if __name__ == "__main__":
    main()
