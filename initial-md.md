## FEATURE: AI Agent Documentation Generator

Generate comprehensive documentation and boilerplate for [PROJECT TYPE]:
- E-commerce platform
- SaaS dashboard
- Marketing website
- Mobile web app
- Internal tool

## REQUIREMENTS:

### Design System (MANDATORY)
- 4 font sizes ONLY (32px, 24px, 16px, 12px)
- 2 font weights ONLY (400, 600)
- 4px grid spacing system
- 60/30/10 color distribution
- Mobile-first (44px+ touch targets)

### Components Needed
- [ ] Authentication flow (login/register/reset)
- [ ] Dashboard layout with navigation
- [ ] Data tables with sorting/filtering
- [ ] Forms with validation
- [ ] File upload with progress
- [ ] Search with autocomplete
- [ ] Settings/profile pages
- [ ] Analytics visualizations

### Business Logic
- User roles: Admin, User, Guest
- Data models: [Specify main entities]
- API structure: RESTful / GraphQL
- Authentication: Supabase / Auth0 / Custom
- State management: React hooks / Zustand

## EXAMPLES:
- See `examples/quiz-component.tsx` for multi-step form pattern
- See `examples/dashboard.tsx` for layout structure
- See `examples/api-client.ts` for error handling

## DOCUMENTATION:
- Supabase docs: https://supabase.com/docs
- Next.js 15 docs: https://nextjs.org/docs
- Framer Motion: https://www.framer.com/motion/

## OTHER CONSIDERATIONS:
- All dates/times in UTC, display in user timezone
- Currency formatting must be locale-aware
- Image uploads max 5MB, auto-compress
- Support dark mode (future consideration)
- Accessibility: WCAG 2.1 AA compliance

## VALIDATION CRITERIA:
The generated documentation must:
1. Include zero design system violations
2. Provide complete TypeScript types
3. Handle all error states
4. Include loading states
5. Work on 320px viewport
6. Pass the validation script
