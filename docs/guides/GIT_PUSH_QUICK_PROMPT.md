# Quick Git Push Prompt - Copy & Paste Version

---

I need you to help me push updates to my Claude Code Boilerplate System. I have two GitHub repositories that must stay synchronized:

**Repos:**
- Private: `git@github.com:bearingfruitco/claude-code-boilerplate.git` (origin)
- Public: `git@github.com:bearingfruitco/cc-boiler-js-public.git` (public)

**Location:** `/Users/shawnsmith/dev/bfc/boilerplate/`

**Security:** Make sure `.gitignore` excludes: `.env`, `.mcp.json`, `node_modules/`, `*.local.json`, logs

**Steps:**
1. Check status: `git status` and `git fetch --all`
2. Stage all: `git add -A`
3. Commit: `git commit --no-verify -m "feat: [your message]"` (use --no-verify if TypeScript errors)
4. Push to BOTH:
   - `git push origin main`
   - `git push public main`
5. Verify: All three hashes should match:
   - `git rev-parse HEAD`
   - `git rev-parse origin/main`
   - `git rev-parse public/main`

Please execute this dual-repository push for me using the Terminal.

---
