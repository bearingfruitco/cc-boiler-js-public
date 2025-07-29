# Create Architecture Command

Design complete system architecture from PRD before generating issues.

## Usage

```bash
/create-architecture
/arch  # alias
```

## Process

I'll leverage the specialized system-architect sub-agent to design your system architecture. First, let me spawn the architect:

```bash
/spawn system-architect
```

The system architect will analyze the PROJECT_PRD.md and create a comprehensive system architecture by:

### 1. PRD Analysis Phase
First, I'll analyze the PRD to extract:
- Core functional requirements
- Data entities and relationships
- User flows and interactions
- Integration requirements
- Performance expectations
- Security requirements

### 2. Architecture Interview
I'll ask key questions about:
- **Technology Stack**: Confirm or suggest optimal technologies
- **Architecture Pattern**: Monolithic, microservices, serverless
- **Data Strategy**: SQL vs NoSQL, caching needs
- **Scaling Requirements**: Expected load, growth projections
- **Integration Preferences**: Third-party services, APIs
- **Development Constraints**: Timeline, team expertise, budget

### 3. Architecture Design
Based on analysis and your input, I'll design:

#### System Components
- Frontend architecture (SSR/CSR/SSG strategy)
- Backend API structure
- Database schema and relationships
- Authentication & authorization flow
- External service integrations
- Infrastructure requirements

#### Technical Decisions
- State management approach
- API design (REST/GraphQL)
- Caching strategy
- Error handling patterns
- Security boundaries
- Performance optimizations

### 4. Documentation Generation
I'll create these documents in `docs/architecture/`:

#### SYSTEM_DESIGN.md
```markdown
# System Architecture - [Project Name]

## Overview
High-level system description and architecture diagram

## Components
- Frontend: Technology, patterns, structure
- Backend: Framework, architecture, APIs
- Database: Technology, schema approach
- Infrastructure: Hosting, CDN, monitoring

## Data Flow
How data moves through the system

## Security Architecture
Authentication, authorization, data protection

## Performance Strategy
Caching, optimization, targets
```

#### DATABASE_SCHEMA.md
- Entity relationship diagrams
- Table definitions
- Indexes and constraints
- Migration strategy

#### API_SPECIFICATION.md
- Endpoint definitions
- Request/response formats
- Authentication requirements
- Rate limiting rules

#### FRONTEND_ARCHITECTURE.md
- Component hierarchy
- State management design
- Routing structure
- Design system integration

#### SECURITY_DESIGN.md
- Threat model
- Security controls
- Compliance requirements
- Data protection measures

#### TECHNICAL_ROADMAP.md
- Implementation phases
- Dependencies
- Risk mitigation
- Timeline estimates

### 5. Component PRP Generation
I'll automatically generate PRPs for major components:
- Database setup and schema
- API implementation
- Frontend structure
- Authentication system
- Third-party integrations
- Admin functionality

### 6. Validation
Finally, I'll:
- Ensure all PRD requirements are addressed
- Check for architectural consistency
- Identify potential risks
- Suggest optimizations

## Expected Output

```
📐 Architecture Design Complete!

Created:
✅ System architecture with [N] components
✅ Database schema with [N] tables
✅ API with [N] endpoints
✅ Frontend with [N] components
✅ [N] component PRPs generated
✅ [N]-phase technical roadmap

Architecture Score: A
- Scalability: ████████░░ 85%
- Security: █████████░ 92%
- Performance: ████████░░ 88%
- Maintainability: █████████░ 90%

Next steps:
1. Review architecture in docs/architecture/
2. Run `/validate-architecture` for detailed analysis
3. Run `/gi PROJECT` to generate implementation issues
4. Use `/fw start 1` to begin Phase 1

The system is properly architected and ready for implementation!
```

## Integration Points

- **After**: `/init-project` creates PRD
- **Before**: `/gi PROJECT` generates issues
- **Works with**: `/create-prp` for components
- **Validated by**: `/validate-architecture`

## Notes

This command ensures thoughtful system design before jumping into code, reducing technical debt and enabling efficient parallel development.
