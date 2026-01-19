# Architecture

**Analysis Date:** 2026-01-19

## Pattern Overview

**Overall:** Next.js App Router (Server Components)

**Key Characteristics:**
- File-based routing using the App Router pattern
- Server-side rendering with React Server Components by default
- Client components via `"use client"` directive where needed
- CSS-in-JS via Tailwind CSS v4 with PostCSS integration
- Type safety through TypeScript with strict mode enabled

## Layers

**Presentation Layer (App Router):**
- Purpose: UI rendering, routing, and user interaction
- Location: `app/`
- Contains: React components, layouts, pages, and stylesheets
- Depends on: Next.js runtime, React, Tailwind CSS
- Used by: End users via web browser

**Asset Layer:**
- Purpose: Static assets served directly
- Location: `public/`
- Contains: Images, icons, static files
- Depends on: None (static files)
- Used by: Application via Next.js asset optimization

**Configuration Layer:**
- Purpose: Build tooling, linting, and development environment setup
- Location: Root directory config files
- Contains: TypeScript config, ESLint config, PostCSS config, Next.js config
- Depends on: Node.js ecosystem
- Used by: Build and development tooling

## Data Flow

**Page Request Flow:**

1. User requests URL (e.g., `/`)
2. Next.js App Router maps URL to `app/page.tsx`
3. Server component renders with React Server Components
4. Root layout (`app/layout.tsx`) wraps page content
5. Tailwind CSS (`app/globals.css`) applies styling
6. HTML response sent to client with hydration data

**Asset Loading Flow:**

1. Component imports asset (e.g., `next/image` for `/next.svg`)
2. Next.js Image Optimization component processes request
3. Asset served from `public/` with optimization applied

**State Management:**
- Server state: Managed by React Server Components (no client-side state)
- Client state: Not implemented (fresh project)
- No external state management library

## Key Abstractions

**Route Segment:**
- Purpose: Represents a URL path and its associated UI
- Examples: `app/page.tsx`, `app/layout.tsx`
- Pattern: File-based routing where directory structure equals URL structure

**Root Layout:**
- Purpose: Shared UI wrapper for all pages
- Implementation: `app/layout.tsx` with font loading and global styles
- Pattern: Server component that wraps all child routes

**Font Optimization:**
- Purpose: Automatic font loading and optimization
- Implementation: `next/font/google` for Geist Sans and Geist Mono
- Pattern: CSS variable injection for font families

**Image Component:**
- Purpose: Optimized image loading with automatic resizing
- Implementation: `next/image` component
- Pattern: Declarative image usage with built-in optimization

## Entry Points

**Application Entry:**
- Location: `app/layout.tsx`
- Triggers: All HTTP requests to the application
- Responsibilities: Root HTML structure, font loading, global style application, metadata definition

**Home Page Entry:**
- Location: `app/page.tsx`
- Triggers: Requests to root path (`/`)
- Responsibilities: Home page UI rendering

**Development Server:**
- Location: Defined in `package.json` scripts
- Triggers: Running `pnpm dev` or `npm run dev`
- Responsibilities: Hot reloading, development build

**Production Build:**
- Location: Defined in `package.json` scripts
- Triggers: Running `pnpm build` or `npm run build`
- Responsibilities: Optimized production bundle generation

## Error Handling

**Strategy:** Not yet implemented (fresh project)

**Patterns:**
- No error boundaries defined
- No custom error pages (`error.tsx` or `not-found.tsx`)
- Relies on Next.js default error handling

## Cross-Cutting Concerns

**Logging:** Not implemented (no custom logging framework)

**Validation:** Not implemented (no form validation or input sanitization)

**Authentication:** Not implemented (no auth system)

**Styling:**
- Framework: Tailwind CSS v4 with PostCSS
- Pattern: Utility-first CSS with CSS variables for theming
- Dark mode: Automatic via `prefers-color-scheme` media query

**Type Safety:**
- TypeScript strict mode enabled
- Type checking at build time
- No runtime validation

---

*Architecture analysis: 2026-01-19*
