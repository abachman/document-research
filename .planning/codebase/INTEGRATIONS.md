# External Integrations

**Analysis Date:** 2025-01-19

## APIs & External Services

**None detected**
- No external API calls found in source code
- No API client libraries in dependencies
- No fetch/axios usage detected in initial codebase scan

## Data Storage

**Databases:**
- None detected

**File Storage:**
- Local filesystem only - Static assets in `/public` directory

**Caching:**
- None detected

## Authentication & Identity

**Auth Provider:**
- None detected

**Implementation:**
- No authentication logic present in codebase
- No auth-related dependencies (next-auth, clerk, etc.)

## Monitoring & Observability

**Error Tracking:**
- None detected

**Logs:**
- Console-based logging (default Next.js behavior)

## CI/CD & Deployment

**Hosting:**
- Vercel (implied) - "Deploy" link to vercel.com in default UI, `.vercel` directory in gitignore

**CI Pipeline:**
- None detected - No GitHub Actions, CI config files, or workflow files present

## Environment Configuration

**Required env vars:**
- None for application runtime
- Note: `mise.local.toml` contains Anthropic API configuration but appears to be development tooling (GSD/Claude Code), not application dependencies

**Secrets location:**
- No secrets management detected
- `.env*` files ignored by git (see `/Users/adambachman/workspace/document-research/.gitignore`)

## Webhooks & Callbacks

**Incoming:**
- None detected

**Outgoing:**
- None detected

## Third-Party Assets

**Fonts:**
- Google Fonts - Geist Sans, Geist Mono (loaded via next/font/google in `/app/layout.tsx`)

**Images:**
- Next.js SVG logos - Local files in `/public` directory
- No CDN-hosted images detected

---

*Integration audit: 2025-01-19*
