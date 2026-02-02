import { test, expect, _electron } from '@playwright/test'
import path from 'path'

/**
 * Basic end-to-end tests for the Document Research Electron app
 *
 * These tests verify:
 * - App launches successfully
 * - IPC bridge initialization and functionality
 * - Database operations work
 */

test.describe('Electron App Launch', () => {
  test('should launch the application successfully', async () => {
    // Launch the Electron app
    const electronApp = await _electron.launch({
      executablePath: path.join(__dirname, '../node_modules/.bin/electron'),
      args: [path.join(__dirname, '../out/main/index.js')],
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
    // Launch the Electron app
    const electronApp = await _electron.launch({
      executablePath: path.join(__dirname, '../node_modules/.bin/electron'),
      args: [path.join(__dirname, '../out/main/index.js')],
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
    const electronApp = await _electron.launch({
      executablePath: path.join(__dirname, '../node_modules/.bin/electron'),
      args: [path.join(__dirname, '../out/main/index.js')],
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

  test('should navigate to IPC test page', async ({ electronApp }) => {
    const window = await electronApp.firstWindow()

    // Try to navigate to the IPC test page
    await window.goto('app://-/electron-ipc-test')

    // Wait for navigation
    await window.waitForLoadState('domcontentloaded')

    // Check if the page loaded successfully
    const url = window.url()
    expect(url).toContain('electron-ipc-test')

    // Check if the test button exists
    const hasTestButton = await window.evaluate(() => {
      const buttons = document.querySelectorAll('button')
      return Array.from(buttons).some(btn => btn.textContent?.includes('Test IPC'))
    })

    expect(hasTestButton).toBe(true)
  })
})
