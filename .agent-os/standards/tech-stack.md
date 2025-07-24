# Tech Stack Standards

## Core Framework
- **Framework**: Next.js 15 (App Router + Turbopack)
- **Runtime**: Node.js 20+
- **Package Manager**: pnpm (preferred), npm, yarn

## Languages & Type Safety
- **Language**: TypeScript (strict mode enforced)
- **Type Checking**: Strict null checks, no implicit any
- **Config**: tsconfig.json with path aliases (@/*)

## Styling & Design
- **CSS Framework**: Tailwind CSS v4
- **CSS Approach**: Utility-first, no custom CSS files
- **Design Tokens**: Custom spacing, font sizes (see design-system.md)
- **Components**: Composition over inheritance

## Database & ORM
- **Database**: Supabase (PostgreSQL)
- **ORM**: Drizzle ORM
- **Migrations**: Drizzle Kit
- **Connection**: Environment variables (DATABASE_URL)

## State Management
- **Client State**: React useState, useReducer
- **Form State**: react-hook-form + zod validation
- **Server State**: React Server Components
- **Global State**: React Context (use sparingly)
- **Storage**: NO localStorage/sessionStorage in artifacts

## Testing
- **Unit Tests**: Vitest
- **Component Tests**: Vitest + React Testing Library
- **E2E Tests**: Playwright
- **Test Approach**: TDD - write tests first
- **Coverage Target**: 80% minimum

## API & Backend
- **API Routes**: Next.js App Router API routes
- **API Client**: Custom fetch wrapper with error handling
- **Authentication**: Supabase Auth (when needed)
- **Rate Limiting**: Built into API routes

## Event System
- **Architecture**: Custom async event queue
- **Events**: Fire-and-forget for non-critical operations
- **Analytics**: Rudderstack integration
- **Error Tracking**: Sentry

## Code Quality
- **Linting**: Biome (replaces ESLint + Prettier)
- **Git Hooks**: Husky + pre-commit validation
- **Commit Format**: Conventional Commits
- **CI/CD**: GitHub Actions

## Development Tools
- **AI Agents**: Claude Code + Cursor
- **Version Control**: Git + GitHub
- **Project Structure**: Feature-based organization
- **Documentation**: Markdown + TSDoc

## Performance
- **Bundler**: Turbopack (Next.js 15)
- **Images**: Next.js Image Optimization
- **Fonts**: Next.js Font Optimization
- **Loading**: Required loading states for all async operations
- **Caching**: React Server Components caching

## Security
- **Environment Variables**: .env.local (never commit)
- **PII Handling**: Field-level encryption
- **TCPA Compliance**: Built-in consent management
- **API Security**: Rate limiting, input validation

## Deployment
- **Platform**: Vercel (preferred)
- **Environment**: Production, Preview, Development
- **Domain**: Custom domains via Vercel
