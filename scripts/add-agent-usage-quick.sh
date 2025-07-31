#!/usr/bin/env bash

# Script to add "When to Use This Agent" sections to all agent files

echo "Adding 'When to Use This Agent' sections to all agent files..."
echo "============================================================"

# Backend agent
cat << 'EOF' > /tmp/backend-usage.txt
## When to Use This Agent

Use the **backend** agent when you need to:
- Create REST API endpoints with proper error handling
- Implement server-side business logic
- Set up authentication and authorization
- Handle file uploads and processing
- Integrate with external services
- Implement webhooks and event handlers
- Create background jobs or scheduled tasks

**Don't use for**: UI components, database schema design, or DevOps tasks.
EOF

# Add to backend.md if not already present
if ! grep -q "## When to Use This Agent" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/backend.md"; then
  # Find line after front matter (---)
  awk '/^---$/ {count++} count==2 {print; print ""; system("cat /tmp/backend-usage.txt"); print ""; next} {print}' \
    "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/backend.md" > /tmp/backend-new.md
  mv /tmp/backend-new.md "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/backend.md"
  echo "✓ Added to backend.md"
else
  echo "✓ backend.md already has usage section"
fi

# Security agent
cat << 'EOF' > /tmp/security-usage.txt
## When to Use This Agent

Use the **security** agent when you need to:
- Perform security audits and vulnerability assessments
- Review authentication and authorization implementations
- Check for OWASP Top 10 vulnerabilities
- Implement security best practices
- Review API security and rate limiting
- Audit data encryption and storage
- Check for PII exposure risks

**Don't use for**: General development tasks or performance optimization.
EOF

if ! grep -q "## When to Use This Agent" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/security.md"; then
  awk '/^---$/ {count++} count==2 {print; print ""; system("cat /tmp/security-usage.txt"); print ""; next} {print}' \
    "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/security.md" > /tmp/security-new.md
  mv /tmp/security-new.md "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/security.md"
  echo "✓ Added to security.md"
else
  echo "✓ security.md already has usage section"
fi

# QA agent
cat << 'EOF' > /tmp/qa-usage.txt
## When to Use This Agent

Use the **qa** agent when you need to:
- Write comprehensive test suites
- Create end-to-end testing scenarios
- Implement test automation
- Review code for bugs and edge cases
- Set up continuous testing pipelines
- Create test documentation
- Validate feature implementations

**Don't use for**: Writing production code or system design.
EOF

if ! grep -q "## When to Use This Agent" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/qa.md"; then
  awk '/^---$/ {count++} count==2 {print; print ""; system("cat /tmp/qa-usage.txt"); print ""; next} {print}' \
    "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/qa.md" > /tmp/qa-new.md
  mv /tmp/qa-new.md "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/qa.md"
  echo "✓ Added to qa.md"
else
  echo "✓ qa.md already has usage section"
fi

# System Architect agent
cat << 'EOF' > /tmp/system-architect-usage.txt
## When to Use This Agent

Use the **system-architect** agent when you need to:
- Design overall system architecture
- Create architectural decision records (ADRs)
- Plan microservices or modular architectures
- Design API contracts and interfaces
- Plan system scalability and reliability
- Create technical roadmaps
- Evaluate technology choices

**Don't use for**: Detailed implementation or coding tasks.
EOF

if ! grep -q "## When to Use This Agent" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/system-architect.md"; then
  awk '/^---$/ {count++} count==2 {print; print ""; system("cat /tmp/system-architect-usage.txt"); print ""; next} {print}' \
    "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/system-architect.md" > /tmp/system-architect-new.md
  mv /tmp/system-architect-new.md "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/system-architect.md"
  echo "✓ Added to system-architect.md"
else
  echo "✓ system-architect.md already has usage section"
fi

# Database Architect agent
cat << 'EOF' > /tmp/database-architect-usage.txt
## When to Use This Agent

Use the **database-architect** agent when you need to:
- Design database schemas and relationships
- Optimize database performance
- Plan data migrations
- Design indexes and query optimization
- Implement data partitioning strategies
- Create data models for new features
- Plan backup and recovery strategies

**Don't use for**: Frontend development or API implementation.
EOF

if ! grep -q "## When to Use This Agent" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/database-architect.md"; then
  awk '/^---$/ {count++} count==2 {print; print ""; system("cat /tmp/database-architect-usage.txt"); print ""; next} {print}' \
    "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/database-architect.md" > /tmp/database-architect-new.md
  mv /tmp/database-architect-new.md "/Users/shawnsmith/dev/bfc/boilerplate/.claude/agents/database-architect.md"
  echo "✓ Added to database-architect.md"
else
  echo "✓ database-architect.md already has usage section"
fi

# Continue with remaining agents...
echo ""
echo "Completed adding usage sections to priority agents."
echo "Run the full Python script to add sections to all remaining agents."

# Clean up temp files
rm -f /tmp/*-usage.txt
