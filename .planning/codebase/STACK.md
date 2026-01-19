# Technology Stack

**Analysis Date:** 2025-01-19

## Languages

**Primary:**
- TypeScript 5.x - All application code in `/app` directory uses TypeScript

**Secondary:**
- CSS - Global styles in `/app/globals.css`
- JavaScript - Configuration files (eslint.config.mjs, postcss.config.mjs)

## Runtime

**Environment:**
- Node.js (via Next.js) - Version managed by pnpm workspace

**Package Manager:**
- pnpm - Lockfile present: `pnpm-lock.yaml`
- Workspace config: `pnpm-workspace.yaml`

## Frameworks

**Core:**
- Next.js 16.1.2 - React framework with App Router (app directory structure)
- React 19.2.3 - UI library
- React DOM 19.2.3 - DOM rendering

**Testing:**
- None detected

**Build/Dev:**
- TypeScript 5.x - Type checking and compilation
- Tailwind CSS 4.x - Utility-first CSS framework
- PostCSS - CSS processing via `postcss.config.mjs`

## Key Dependencies

**Critical:**
- next/font/google - Google Fonts integration (Geist, Geist_Mono fonts in `/app/layout.tsx`)
- next/image - Image optimization component

**Infrastructure:**
- None detected

## Configuration

**Environment:**
- TypeScript: `tsconfig.json` (ES2017 target, strict mode, bundler module resolution)
- Path aliases: `@/*` maps to project root
- No `.env` files detected (all ignored by git)

**Build:**
- Next.js config: `next.config.ts` (minimal/default configuration)
- PostCSS config: `postcss.config.mjs` (Tailwind CSS plugin)
- ESLint config: `eslint.config.mjs` (Next.js core web vitals + TypeScript presets)

## Platform Requirements

**Development:**
- Node.js (for Next.js runtime)
- pnpm package manager
- TypeScript compiler (via tsc or Next.js built-in)

**Production:**
- Node.js server (for Next.js server-side rendering)
- Vercel deployment ready (Deploy link present in default UI)

---

*Stack analysis: 2025-01-19*
