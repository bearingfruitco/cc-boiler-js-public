#!/usr/bin/env bash

# Add "When to Use This Agent" sections to all agent files

AGENTS_DIR="/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents"

# Function to add usage section to a file
add_usage_section() {
    local file="$1"
    local content="$2"
    
    if ! grep -q "## When to Use This Agent" "$file"; then
        # Create temp file with new content
        awk -v usage="$content" '
            /^---$/ {count++} 
            count==2 && !inserted {
                print; 
                print ""; 
                print usage; 
                print ""; 
                inserted=1; 
                next
            } 
            {print}
        ' "$file" > "${file}.tmp"
        
        mv "${file}.tmp" "$file"
        echo "✓ Added to $(basename "$file")"
    else
        echo "✓ $(basename "$file") already has usage section"
    fi
}

echo "Adding 'When to Use This Agent' sections..."
echo "=========================================="

# Add sections to each agent file

# Backend
add_usage_section "$AGENTS_DIR/backend.md" "## When to Use This Agent

Use the **backend** agent when you need to:
- Create REST API endpoints with proper error handling
- Implement server-side business logic
- Set up authentication and authorization
- Handle file uploads and processing
- Integrate with external services
- Implement webhooks and event handlers
- Create background jobs or scheduled tasks

**Don't use for**: UI components, database schema design, or DevOps tasks."

# Security
add_usage_section "$AGENTS_DIR/security.md" "## When to Use This Agent

Use the **security** agent when you need to:
- Perform security audits and vulnerability assessments
- Review authentication and authorization implementations
- Check for OWASP Top 10 vulnerabilities
- Implement security best practices
- Review API security and rate limiting
- Audit data encryption and storage
- Check for PII exposure risks

**Don't use for**: General development tasks or performance optimization."

# QA
add_usage_section "$AGENTS_DIR/qa.md" "## When to Use This Agent

Use the **qa** agent when you need to:
- Write comprehensive test suites
- Create end-to-end testing scenarios
- Implement test automation
- Review code for bugs and edge cases
- Set up continuous testing pipelines
- Create test documentation
- Validate feature implementations

**Don't use for**: Writing production code or system design."

# System Architect
add_usage_section "$AGENTS_DIR/system-architect.md" "## When to Use This Agent

Use the **system-architect** agent when you need to:
- Design overall system architecture
- Create architectural decision records (ADRs)
- Plan microservices or modular architectures
- Design API contracts and interfaces
- Plan system scalability and reliability
- Create technical roadmaps
- Evaluate technology choices

**Don't use for**: Detailed implementation or coding tasks."

# Database Architect
add_usage_section "$AGENTS_DIR/database-architect.md" "## When to Use This Agent

Use the **database-architect** agent when you need to:
- Design database schemas and relationships
- Optimize database performance
- Plan data migrations
- Design indexes and query optimization
- Implement data partitioning strategies
- Create data models for new features
- Plan backup and recovery strategies

**Don't use for**: Frontend development or API implementation."

# Supabase Specialist
add_usage_section "$AGENTS_DIR/supabase-specialist.md" "## When to Use This Agent

Use the **supabase-specialist** agent when you need to:
- Set up Supabase projects and configuration
- Implement Row Level Security (RLS) policies
- Create database functions and triggers
- Set up real-time subscriptions
- Configure Supabase Auth
- Optimize Supabase queries
- Integrate Supabase with your application

**Don't use for**: General database design or non-Supabase backends."

# Form Builder Specialist
add_usage_section "$AGENTS_DIR/form-builder-specialist.md" "## When to Use This Agent

Use the **form-builder-specialist** agent when you need to:
- Create complex multi-step forms
- Implement advanced form validation
- Build dynamic form fields
- Handle file uploads in forms
- Create accessible form experiences
- Implement form state management
- Build survey or questionnaire systems

**Don't use for**: Simple forms (use frontend agent) or backend processing."

# UI Systems
add_usage_section "$AGENTS_DIR/ui-systems.md" "## When to Use This Agent

Use the **ui-systems** agent when you need to:
- Create reusable design system components
- Implement component libraries
- Build Storybook documentation
- Ensure design consistency across components
- Create component APIs and props
- Build accessible component patterns
- Implement theming systems

**Don't use for**: Page-level implementations or business logic."

# Performance
add_usage_section "$AGENTS_DIR/performance.md" "## When to Use This Agent

Use the **performance** agent when you need to:
- Analyze and fix performance bottlenecks
- Optimize bundle sizes
- Improve page load times
- Implement caching strategies
- Optimize database queries
- Profile application performance
- Set up performance monitoring

**Don't use for**: Feature development or bug fixes."

# Analyzer
add_usage_section "$AGENTS_DIR/analyzer.md" "## When to Use This Agent

Use the **analyzer** agent when you need to:
- Perform deep code analysis
- Trace code execution paths
- Debug complex issues
- Analyze dependencies and imports
- Review code quality and patterns
- Identify code smells
- Analyze performance bottlenecks

**Don't use for**: Writing new features or refactoring."

# Refactoring Expert
add_usage_section "$AGENTS_DIR/refactoring-expert.md" "## When to Use This Agent

Use the **refactoring-expert** agent when you need to:
- Refactor legacy code
- Improve code organization
- Implement design patterns
- Reduce code duplication
- Simplify complex functions
- Improve code maintainability
- Modernize old code patterns

**Don't use for**: Adding new features or fixing bugs."

# Platform Deployment
add_usage_section "$AGENTS_DIR/platform-deployment.md" "## When to Use This Agent

Use the **platform-deployment** agent when you need to:
- Set up CI/CD pipelines
- Configure deployment environments
- Optimize Docker containers
- Set up monitoring and logging
- Configure CDN and caching
- Implement blue-green deployments
- Troubleshoot deployment issues

**Don't use for**: Application development or database design."

# Integration Specialist
add_usage_section "$AGENTS_DIR/integration-specialist.md" "## When to Use This Agent

Use the **integration-specialist** agent when you need to:
- Integrate with third-party APIs
- Implement webhooks
- Set up OAuth flows
- Handle API authentication
- Transform data between systems
- Implement retry and circuit breaker patterns
- Build API clients

**Don't use for**: Internal API development or UI work."

# Documentation Writer
add_usage_section "$AGENTS_DIR/documentation-writer.md" "## When to Use This Agent

Use the **documentation-writer** agent when you need to:
- Write technical documentation
- Create API documentation
- Write user guides
- Document code and architectures
- Create README files
- Write migration guides
- Document best practices

**Don't use for**: Code implementation or system design."

# Migration Specialist
add_usage_section "$AGENTS_DIR/migration-specialist.md" "## When to Use This Agent

Use the **migration-specialist** agent when you need to:
- Plan and execute database migrations
- Migrate between frameworks or libraries
- Update dependency versions
- Migrate data between systems
- Handle breaking changes
- Create rollback procedures
- Document migration steps

**Don't use for**: New feature development or performance optimization."

# ORM Specialist
add_usage_section "$AGENTS_DIR/orm-specialist.md" "## When to Use This Agent

Use the **orm-specialist** agent when you need to:
- Optimize ORM queries (Drizzle, Prisma)
- Design ORM schemas
- Implement complex queries
- Handle ORM migrations
- Optimize query performance
- Implement ORM best practices
- Debug ORM issues

**Don't use for**: Raw SQL queries or frontend development."

# PM Orchestrator
add_usage_section "$AGENTS_DIR/pm-orchestrator.md" "## When to Use This Agent

Use the **pm-orchestrator** agent when you need to:
- Break down complex requirements
- Create project roadmaps
- Prioritize features
- Coordinate between technical and business needs
- Create user stories
- Plan sprints and milestones
- Facilitate technical decisions

**Don't use for**: Direct implementation or coding tasks."

# PRD Writer
add_usage_section "$AGENTS_DIR/prd-writer.md" "## When to Use This Agent

Use the **prd-writer** agent when you need to:
- Write comprehensive PRDs
- Document feature requirements
- Create acceptance criteria
- Define success metrics
- Document user flows
- Create mockups and wireframes
- Define MVP scope

**Don't use for**: Technical implementation or code writing."

# PRP Writer
add_usage_section "$AGENTS_DIR/prp-writer.md" "## When to Use This Agent

Use the **prp-writer** agent when you need to:
- Convert PRDs to technical PRPs
- Create implementation-ready specs
- Define technical requirements
- Break down features into tasks
- Create technical acceptance criteria
- Document implementation approaches
- Define testing strategies

**Don't use for**: High-level planning or actual coding."

# Analytics Engineer
add_usage_section "$AGENTS_DIR/analytics-engineer.md" "## When to Use This Agent

Use the **analytics-engineer** agent when you need to:
- Set up analytics tracking
- Implement event schemas
- Configure analytics tools
- Create data pipelines
- Build analytics dashboards
- Implement privacy-compliant tracking
- Debug tracking issues

**Don't use for**: Frontend UI or backend API development."

# Event Schema
add_usage_section "$AGENTS_DIR/event-schema.md" "## When to Use This Agent

Use the **event-schema** agent when you need to:
- Design event taxonomies
- Create tracking plans
- Define event properties
- Implement event validation
- Document event flows
- Plan analytics architecture
- Ensure event consistency

**Don't use for**: Implementation of tracking code or UI development."

# Privacy Compliance
add_usage_section "$AGENTS_DIR/privacy-compliance.md" "## When to Use This Agent

Use the **privacy-compliance** agent when you need to:
- Implement GDPR compliance
- Create privacy policies
- Handle consent management
- Implement data deletion
- Audit PII handling
- Create cookie policies
- Implement privacy controls

**Don't use for**: General development or performance tasks."

# Playwright Specialist
add_usage_section "$AGENTS_DIR/playwright-specialist.md" "## When to Use This Agent

Use the **playwright-specialist** agent when you need to:
- Write browser automation tests
- Create end-to-end test suites
- Implement visual regression tests
- Debug browser-specific issues
- Test complex user interactions
- Set up cross-browser testing
- Create test fixtures

**Don't use for**: Unit testing or API testing."

# TDD Engineer
add_usage_section "$AGENTS_DIR/tdd-engineer.md" "## When to Use This Agent

Use the **tdd-engineer** agent when you need to:
- Implement test-driven development
- Write tests before code
- Create comprehensive test suites
- Refactor with test coverage
- Implement testing best practices
- Set up testing frameworks
- Coach on TDD practices

**Don't use for**: Writing code without tests or quick prototypes."

# Mentor
add_usage_section "$AGENTS_DIR/mentor.md" "## When to Use This Agent

Use the **mentor** agent when you need to:
- Learn new technologies
- Understand best practices
- Get code review feedback
- Improve coding skills
- Understand design patterns
- Learn system design
- Get career guidance

**Don't use for**: Direct implementation or urgent fixes."

# Financial Analyst
add_usage_section "$AGENTS_DIR/financial-analyst.md" "## When to Use This Agent

Use the **financial-analyst** agent when you need to:
- Analyze project costs
- Create budget estimates
- Evaluate technical debt
- Plan resource allocation
- Analyze ROI of features
- Create cost projections
- Optimize cloud spending

**Don't use for**: Technical implementation or design tasks."

# Researcher
add_usage_section "$AGENTS_DIR/researcher.md" "## When to Use This Agent

Use the **researcher** agent when you need to:
- Research new technologies
- Evaluate technical solutions
- Compare frameworks or tools
- Research best practices
- Investigate technical problems
- Find documentation
- Evaluate third-party services

**Don't use for**: Implementation or hands-on coding."

# Senior Engineer
add_usage_section "$AGENTS_DIR/senior-engineer.md" "## When to Use This Agent

Use the **senior-engineer** agent when you need to:
- Solve complex technical problems
- Make architectural decisions
- Review critical code
- Mentor other developers
- Handle production issues
- Design scalable solutions
- Lead technical initiatives

**Don't use for**: Simple tasks or basic implementations."

# Code Reviewer
add_usage_section "$AGENTS_DIR/code-reviewer.md" "## When to Use This Agent

Use the **code-reviewer** agent when you need to:
- Review pull requests
- Check code quality
- Ensure best practices
- Identify potential bugs
- Suggest improvements
- Validate architecture decisions
- Ensure code standards

**Don't use for**: Writing new code or implementing features."

# Production Code Validator
add_usage_section "$AGENTS_DIR/production-code-validator.md" "## When to Use This Agent

Use the **production-code-validator** agent when you need to:
- Validate production readiness
- Check for security issues
- Ensure error handling
- Validate logging and monitoring
- Check performance implications
- Ensure scalability
- Validate deployment configuration

**Don't use for**: Development or design tasks."

# PII Guardian
add_usage_section "$AGENTS_DIR/pii-guardian.md" "## When to Use This Agent

Use the **pii-guardian** agent when you need to:
- Audit PII handling
- Implement data masking
- Review data storage
- Ensure PII compliance
- Create data policies
- Implement data encryption
- Audit logging for PII

**Don't use for**: General security or development tasks."

# Automation Workflow Engineer
add_usage_section "$AGENTS_DIR/automation-workflow-engineer.md" "## When to Use This Agent

Use the **automation-workflow-engineer** agent when you need to:
- Create automated workflows
- Set up CI/CD pipelines
- Implement task automation
- Create scheduled jobs
- Build workflow orchestration
- Automate repetitive tasks
- Create automation scripts

**Don't use for**: Manual tasks or UI development."

# Report Generator
add_usage_section "$AGENTS_DIR/report-generator.md" "## When to Use This Agent

Use the **report-generator** agent when you need to:
- Generate project reports
- Create status updates
- Build analytics reports
- Generate documentation
- Create dashboards
- Export data reports
- Automate reporting

**Don't use for**: Real-time features or interactive UIs."

# Progress Logger
add_usage_section "$AGENTS_DIR/progress-logger.md" "## When to Use This Agent

Use the **progress-logger** agent when you need to:
- Track project progress
- Log development activities
- Create progress reports
- Monitor task completion
- Track time spent
- Document progress
- Create burndown charts

**Don't use for**: Implementation or feature development."

echo ""
echo "✅ Completed adding 'When to Use This Agent' sections!"
echo "Total agents processed: $(ls $AGENTS_DIR/*.md | grep -v QUICK_REFERENCE | grep -v agent-tool | wc -l)"
