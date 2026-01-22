import { ipcMain, app } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'
import { db, initializeSchema } from './database.js'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

/**
 * Validate sender frame URL to prevent unauthorized access
 * Only allows requests from:
 * - Local app files (app:// protocol in production)
 * - Development server (http://localhost:3000)
 */
function validateSender(frame: { url: string }): boolean {
  const allowedOrigins = [
    'app://-',           // Production: electron-serve protocol
    'http://localhost:3000'  // Development: Next.js dev server
  ]

  const isAllowed = allowedOrigins.some(origin => frame.url.startsWith(origin))

  if (!isAllowed) {
    console.warn(`[Security] Unauthorized IPC request from: ${frame.url}`)
  }

  return isAllowed
}

/**
 * Register all IPC handlers for database operations
 */
export function registerHandlers(): void {
  // Handler for executing SQL statements (INSERT, UPDATE, DELETE)
  ipcMain.handle('db:exec', (event, sql: string, params: unknown[] = []) => {
    if (!event.senderFrame || !validateSender(event.senderFrame)) {
      throw new Error('Unauthorized: Invalid sender origin')
    }

    try {
      const stmt = db.prepare(sql)
      const result = stmt.run(...params)

      // Return both lastInsertRowid and changes count
      return {
        success: true,
        lastInsertRowid: result.lastInsertRowid,
        changes: result.changes
      }
    } catch (error) {
      console.error('[IPC] db:exec error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  })

  // Handler for executing SELECT queries
  ipcMain.handle('db:query', (event, sql: string, params: unknown[] = []) => {
    if (!event.senderFrame || !validateSender(event.senderFrame)) {
      throw new Error('Unauthorized: Invalid sender origin')
    }

    try {
      const stmt = db.prepare(sql)
      const results = stmt.all(...params)

      return {
        success: true,
        data: results
      }
    } catch (error) {
      console.error('[IPC] db:query error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        data: []
      }
    }
  })

  // Handler for initializing database schema
  ipcMain.handle('db:init', (event) => {
    if (!event.senderFrame || !validateSender(event.senderFrame)) {
      throw new Error('Unauthorized: Invalid sender origin')
    }

    try {
      initializeSchema()

      return {
        success: true,
        message: 'Database schema initialized successfully'
      }
    } catch (error) {
      console.error('[IPC] db:init error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  })

  console.log('[IPC] Database handlers registered')
}
