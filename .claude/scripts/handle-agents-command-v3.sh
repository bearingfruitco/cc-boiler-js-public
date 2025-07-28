#!/bin/bash
# Enhanced /agents command handler for v3.0

# Check if user typed /agents
if [[ "$CLAUDE_USER_PROMPT" =~ ^/agents ]]; then
    echo "📊 Claude Code Boilerplate v3.0 - Agent System"
    echo "============================================="
    echo ""
    echo "🤖 Total Agents: 31"
    echo ""
    echo "📁 Technology Specialists (v3.0 - NEW):"
    echo "  • supabase-specialist - Supabase, RLS, auth, realtime"
    echo "  • orm-specialist - Drizzle/Prisma schema & migrations"
    echo "  • analytics-engineer - RudderStack, BigQuery, DBT"
    echo "  • ui-systems - Shadcn UI, Tailwind 4, Framer Motion"
    echo "  • privacy-compliance - GDPR, CCPA, TCPA, consent"
    echo "  • event-schema - Event taxonomy, PII classification"
    echo "  • platform-deployment - Vercel, GCP, edge functions"
    echo ""
    echo "👥 Role-Based Agents (v2.8.0):"
    echo "  • pm-orchestrator - Project coordination"
    echo "  • senior-engineer - Architecture & best practices"
    echo "  • backend/frontend - API & UI development"
    echo "  • qa/security - Testing & security"
    echo "  • database-architect - DB design"
    echo "  • ...and 17 more specialists"
    echo ""
    echo "🚀 Quick Commands:"
    echo "  • /at <task> - Analyze task & recommend agents"
    echo "  • /orchestrate <task> - Multi-agent coordination"
    echo "  • /agent-health - Check all agents status"
    echo "  • /chains - View workflow chains"
    echo ""
    echo "💡 Try: '/at build a secure auth system with analytics'"
    
    # Log agent command usage
    echo "{\"event\": \"agents_command\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> .claude/logs/agent-usage.jsonl
fi
