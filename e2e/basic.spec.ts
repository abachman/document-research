import { test, expect, _electron } from '@playwright/test'
import { findLatestBuild, parseElectronApp } from 'electron-playwright-helpers'

/**
 * Basic end-to-end tests for the Document Research Electron app
 *
 * These tests verify:
 * - App launches successfully
 * - IPC bridge initialization and functionality
 * - Database operations work
 * - Python service API availability
 *
 * Total tests: 6
 */

test.describe('Electron App Launch', () => {
  test('should launch the application successfully', async () => {
    // Find the latest build and parse app info
    const latestBuild = findLatestBuild('out')
    const appInfo = parseElectronApp(latestBuild)

    // Launch the Electron app
    const electronApp = await _electron.launch({
      executablePath: appInfo.executable,
      args: [appInfo.main, '--no-sandbox', '--disable-dev-shm-usage'],
    })

    // Get the first window (main window)
    const window = await electronApp.firstWindow()

    // Check if the window is visible
    expect(await window.evaluate(() => {
      return document.visibilityState === 'visible'
    })).toBe(true)

    // Verify window has loaded
    const title = await window.title()
    expect(title).toBeTruthy()

    // Clean up
    await electronApp.close()
  })

  test('should display page with expected content', async () => {
    // Find the latest build and parse app info
    const latestBuild = findLatestBuild('out')
    const appInfo = parseElectronApp(latestBuild)

    // Launch the Electron app
    const electronApp = await _electron.launch({
      executablePath: appInfo.executable,
      args: [appInfo.main, '--no-sandbox', '--disable-dev-shm-usage'],
    })

    // Get the first window
    const window = await electronApp.firstWindow()

    // Wait for page to be fully loaded
    await window.waitForLoadState('domcontentloaded')

    // Check if we can access the DOM
    const bodyText = await window.evaluate(() => document.body.innerText)
    expect(bodyText).toBeTruthy()

    // Clean up
    await electronApp.close()
  })
})

test.describe('IPC Bridge Functionality', () => {
  test.use({ electronApp: async ({}, use) => {
    // Setup: Launch Electron app for all tests in this describe block
    const latestBuild = findLatestBuild('out')
    const appInfo = parseElectronApp(latestBuild)
    const electronApp = await _electron.launch({
      executablePath: appInfo.executable,
      args: [appInfo.main],
    })
    await use(electronApp)
    // Teardown: Close app after tests
    await electronApp.close()
  }})

  test('should have electronAPI exposed in renderer process', async ({ electronApp }) => {
    const window = await electronApp.firstWindow()

    // Check if window.electronAPI is available
    const hasElectronAPI = await window.evaluate(() => {
      return typeof (window as any).electronAPI !== 'undefined'
    })

    expect(hasElectronAPI).toBe(true)
  })

  test('should initialize database successfully', async ({ electronApp }) => {
    const window = await electronApp.firstWindow()

    // Initialize database
    const initResult = await window.evaluate(async () => {
      try {
        const result = await (window as any).electronAPI.initDatabase()
        return { success: result.success, message: result.message }
      } catch (error) {
        return { success: false, error: String(error) }
      }
    })

    expect(initResult.success).toBe(true)
  })

  test('should execute database operations', async ({ electronApp }) => {
    const window = await electronApp.firstWindow()

    // First initialize database
    await window.evaluate(async () => {
      await (window as any).electronAPI.initDatabase()
    })

    // Insert test data
    const insertResult = await window.evaluate(async () => {
      try {
        const result = await (window as any).electronAPI.execDatabase(
          'INSERT INTO annotations (type, text, position) VALUES (?, ?, ?)',
          ['test-highlight', 'Test annotation text', '{"page": 1}']
        )
        return { success: result.success, lastInsertRowid: result.lastInsertRowid }
      } catch (error) {
        return { success: false, error: String(error) }
      }
    })

    expect(insertResult.success).toBe(true)
    expect(insertResult.lastInsertRowid).toBeGreaterThan(0)

    // Query the data back
    const queryResult = await window.evaluate(async () => {
      try {
        const result = await (window as any).electronAPI.queryDatabase(
          'SELECT * FROM annotations WHERE type = ?',
          ['test-highlight']
        )
        return { success: result.success, data: result.data }
      } catch (error) {
        return { success: false, error: String(error) }
      }
    })

    expect(queryResult.success).toBe(true)
    expect(Array.isArray(queryResult.data)).toBe(true)
    expect(queryResult.data.length).toBeGreaterThan(0)
  })

  test('should have Python service API available', async ({ electronApp }) => {
    const window = await electronApp.firstWindow()

    // Check if Python service API exists
    const hasPythonAPI = await window.evaluate(() => {
      const api = (window as any).electronAPI
      return api && typeof api.python === 'object'
    })

    expect(hasPythonAPI).toBe(true)
  })
})
