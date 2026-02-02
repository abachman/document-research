import { defineConfig, devices } from '@playwright/test'
import path from 'path'
import electron from 'electron'

/**
 * Playwright configuration for Electron end-to-end testing
 *
 * This config is specifically set up for testing the Electron app, not web testing.
 * Tests will launch the actual Electron application and interact with the renderer process.
 *
 * Note: Playwright's Electron support uses the _electron.launch() API in test files,
 * not the traditional web browser approach.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false, // Electron tests should run sequentially
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // Run tests one at a time for Electron
  reporter: 'html',

  // Electron takes longer to start than web apps
  timeout: 30000,

  use: {
    // Capture screenshot on failure
    screenshot: 'only-on-failure',

    // Record video on failure for debugging
    video: 'retain-on-failure',

    // Trace on failure for detailed debugging
    trace: 'retain-on-failure',
  },

  projects: [
    {
      name: 'electron',
      use: {
        // Electron-specific configuration
        // Tests will use _electron.launch() to start the app
      },
    },
  ],
})
