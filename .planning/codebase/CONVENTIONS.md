# Coding Conventions

**Analysis Date:** 2026-01-19

## Naming Patterns

**Files:**
- Components: PascalCase (e.g., `page.tsx`, `layout.tsx`)
- Config files: kebab-case or dot-prefixed (e.g., `next.config.ts`, `eslint.config.mjs`)
- Global styles: kebab-case with `global` prefix (e.g., `globals.css`)

**Functions:**
- Components: PascalCase for default exports (e.g., `export default function Home()`)
- Font configurations: camelCase (e.g., `geistSans`, `geistMono`)

**Variables:**
- camelCase for local variables (e.g., `variable`, `subsets`)
- kebab-case for CSS variables (e.g., `--font-geist-sans`, `--background`)

**Types:**
- PascalCase for TypeScript types and interfaces (e.g., `Metadata`, `Readonly`, `React.ReactNode`)

## Code Style

**Formatting:**
- No explicit Prettier configuration detected
- Next.js default formatting conventions applied
- Indentation appears to be 2 spaces (based on file structure)

**Linting:**
- ESLint 9.x with flat config format (`eslint.config.mjs`)
- Uses `eslint-config-next` with `core-web-vitals` and `typescript` presets
- Config extends Next.js recommended rules for TypeScript
- Run: `pnpm lint` or `npm run lint`

**Key ESLint settings:**
- TypeScript strict mode enabled
- Next.js specific rules applied
- Global ignores: `.next/**`, `out/**`, `build/**`, `next-env.d.ts`

## Import Organization

**Order:**
1. Type imports (with `import type` syntax)
2. Named imports from external packages
3. Relative imports (styles, components)

**Examples from `app/layout.tsx`:**
```typescript
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
```

**Path Aliases:**
- `@/*` maps to project root (configured in `tsconfig.json`)
- Example: `@/components/Button` would resolve to `./components/Button`

## Error Handling

**Patterns:**
- No explicit error handling patterns detected in current codebase
- Uses TypeScript's strict mode for compile-time error prevention
- Next.js provides default error boundaries

**TypeScript Strict Mode:**
- `strict: true` in `tsconfig.json`
- `noEmit: true` for compilation without output
- Enables all strict type checking options

## Logging

**Framework:** Not explicitly configured (no dedicated logging library detected)

**Patterns:**
- No logging patterns observed in current codebase
- Would rely on browser console for development
- Next.js provides built-in development logging

## Comments

**When to Comment:**
- Minimal usage in current codebase
- Code is largely self-documenting through TypeScript types

**JSDoc/TSDoc:**
- Not extensively used in current codebase
- Type annotations provide most documentation
- Next.js generated files include inline comments (e.g., `next-env.d.ts`)

## Function Design

**Size:**
- Component functions kept focused and modular
- `Home` component in `app/page.tsx`: ~60 lines
- `RootLayout` component in `app/layout.tsx`: ~35 lines

**Parameters:**
- Destructured props with TypeScript type annotations
- Example from `app/layout.tsx`:
```typescript
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
```

**Return Values:**
- Components return JSX with consistent formatting
- Uses React functional components with hooks pattern

## Module Design

**Exports:**
- Default exports for page and layout components
- Named exports for metadata and font configurations
- Example from `app/layout.tsx`:
```typescript
export const metadata: Metadata = { ... };
export default function RootLayout({ ... }) { ... }
```

**Barrel Files:**
- Not currently used (codebase is minimal with direct imports)

## TypeScript Configuration

**Key Settings:**
- Target: ES2017
- Module resolution: `bundler` (Next.js optimized)
- JSX: `react-jsx` (automatic runtime)
- Incremental compilation enabled
- Path aliases configured for `@/*`

**Type Import Pattern:**
- Prefer `import type` for type-only imports
- Reduces bundle size and clarifies intent

## CSS/Styling Conventions

**Framework:** Tailwind CSS v4 with PostCSS

**Pattern:**
- Utility-first CSS classes
- Inline class strings (no separate CSS modules)
- Dark mode support via `dark:` prefix
- CSS variables for theming in `globals.css`

**Example from `app/page.tsx`:**
```tsx
className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black"
```

**CSS Variables:**
- Defined in `:root` in `globals.css`
- Referenced in Tailwind config via `@theme inline`
- Supports light/dark mode via media query

---

*Convention analysis: 2026-01-19*
