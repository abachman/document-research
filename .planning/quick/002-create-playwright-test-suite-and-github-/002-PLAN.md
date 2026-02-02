---
phase: quick-002
plan: 002
type: execute
wave: 1
depends_on: []
files_modified: [package.json, playwright.config.ts, .github/workflows/test.yml]
autonomous: true

must_haves:
  truths:
    - "Playwright can run end-to-end tests against the Electron app"
    - "GitHub Actions runs tests automatically on push/PR"
    - "Tests verify basic app functionality (IPC bridge, database operations)"
  artifacts:
    - path: "e2e/basic.spec.ts"
      provides: "End-to-end tests for Electron app"
      contains: "test('IPC bridge works')"
    - path: "playwright.config.ts"
      provides: "Playwright configuration for Electron testing"
      exports: ["defineConfig"]
    - path: ".github/workflows/test.yml"
      provides: "GitHub Actions workflow for CI/CD"
      contains: "on: [push, pull_request]"
  key_links:
    - from: ".github/workflows/test.yml"
      to: "e2e/basic.spec.ts"
      via: "npm run test:e2e"
      pattern: "run:.*test:e2e"
---

<objective>
Add Playwright end-to-end testing framework and GitHub Actions CI/CD workflow

Purpose: Ensure application reliability through automated testing and catch regressions early
Output: Working test suite with CI pipeline
</objective>

<execution_context>
@./.claude/get-shit-done/workflows/execute-plan.md
@./.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/STATE.md
@/Users/adambachman/workspace/document-research/app/lib/electron.ts
@/Users/adambachman/workspace/document-research/app/electron-ipc-test/page.tsx
@/Users/adambachman/workspace/document-research/package.json
</context>

<tasks>

<task type="auto">
  <name>Task 1: Install and configure Playwright for Electron testing</name>
  <files>package.json, playwright.config.ts</files>
  <action>
    Install Playwright with Electron support:
    - Run: `npm install -D @playwright/test`
    - Add to package.json scripts:
      * "test:e2e": "playwright test"
      * "test:e2e:ui": "playwright test --ui"
      * "test:e2e:debug": "playwright test --debug"

    Create playwright.config.ts in project root:
    - Use @playwright/test electron launcher
    - Configure testDir: './e2e'
    - Set timeout: 30000 (Electron app takes longer to start)
    - Enable video: 'retain-on-failure' for debugging
    - Use Electron mode: point to 'out/main/index.js'

    DO NOT use web-only Playwright config - this is an Electron app
  </action>
  <verify>cat playwright.config.ts shows electron.launcher() configuration</verify>
  <done>Playwright installed with Electron support, configuration file created</done>
</task>

<task type="auto">
  <name>Task 2: Create basic end-to-end test suite</name>
  <files>e2e/basic.spec.ts</files>
  <action>
    Create e2e/basic.spec.ts with tests for:

    Test 1: App launches successfully
    - Launch Electron app
    - Verify window is visible
    - Check page title contains "Document Research"

    Test 2: IPC bridge initialization
    - Navigate to /electron-ipc-test
    - Click "Test IPC" button
    - Verify console shows "Database initialized"
    - Verify console shows "Insert successful"
    - Verify query returns results (not empty)

    Test 3: Python service API availability (optional, if time permits)
    - Check window.electronAPI.python exists
    - Verify getPort() returns success

    Use Playwright's page.evaluate() to access window.electronAPI
    Use expect() from @playwright/test for assertions
    Add test.beforeEach() to setup fresh app state
  </action>
  <verify>
    - e2e/basic.spec.ts exists with 2-3 tests
    - Run: npm run test:e2e (should pass if Electron app builds correctly)
  </verify>
  <done>Test suite covers app launch and IPC bridge functionality</done>
</task>

<task type="auto">
  <name>Task 3: Create GitHub Actions workflow for CI/CD</name>
  <files>.github/workflows/test.yml</files>
  <action>
    Create .github/workflows/test.yml with:

    Trigger conditions:
    - on: push (branches: [main, develop])
    - on: pull_request (branches: [main])

    Job configuration:
    - runs-on: macos-latest (Electron tests need macOS/Windows/Linux GUI)
    - timeout-minutes: 15

    Steps:
    1. Checkout code (actions/checkout@v4)
    2. Setup Node.js (actions/setup-node@v4 with node-version-file: package.json)
    3. Install dependencies (npm ci or pnpm install)
    4. Install Python 3.13 (actions/setup-python@v4 with python-version: '3.13')
    5. Install Python dependencies (pip install -r python-service/requirements.txt)
    6. Install Playwright browsers (npx playwright install --with-deps)
    7. Build Electron app (npm run build)
    8. Run E2E tests (npm run test:e2e)
    9. Upload test artifacts (test results, videos on failure)

    Matrix strategy (optional enhancement):
    - Test on macOS, Windows, Ubuntu if needed for v1

    DO NOT skip Python setup - app depends on ML service
  </action>
  <verify>
    - .github/workflows/test.yml exists
    - File contains 8-10 steps in correct order
    - YAML is valid (no syntax errors)
  </verify>
  <done>GitHub Actions workflow configured to run tests on push/PR</done>
</task>

</tasks>

<verification>
Overall phase checks:
- [ ] Playwright installs successfully with Electron support
- [ ] Configuration file uses electron.launcher() (not web config)
- [ ] Test file e2e/basic.spec.ts has at least 2 tests
- [ ] Tests verify IPC bridge functionality (window.electronAPI access)
- [ ] GitHub Actions workflow includes all required steps
- [ ] YAML syntax is valid (cat .github/workflows/test.yml shows proper structure)
- [ ] Workflow includes Python setup (required for ML service)
</verification>

<success_criteria>
Measurable completion:
- `npm run test:e2e` runs successfully (tests may fail if Electron not built, but runner executes)
- `cat playwright.config.ts` shows valid Electron configuration
- `cat e2e/basic.spec.ts` shows at least 2 test cases
- `cat .github/workflows/test.yml` shows complete workflow with 8+ steps
- Git status shows 3 new files: playwright.config.ts, e2e/basic.spec.ts, .github/workflows/test.yml
</success_criteria>

<output>
After completion, create `.planning/quick/002-create-playwright-test-suite-and-github-/002-SUMMARY.md`
</output>
