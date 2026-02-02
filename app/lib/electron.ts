/**
 * TypeScript types for Electron API exposed via contextBridge
 * Provides autocomplete and type safety for renderer process database access
 *
 * This file augments the global Window interface to include electronAPI
 * Usage in components: await window.electronAPI.queryDatabase('SELECT * FROM documents')
 */

/**
 * Result structure returned by database query operations
 */
export interface DatabaseQueryResult {
  success: boolean
  data: unknown[]
  error?: string
}

/**
 * Result structure returned by database exec operations (INSERT/UPDATE/DELETE)
 */
export interface DatabaseExecResult {
  success: boolean
  lastInsertRowid: number
  changes: number
  error?: string
}

/**
 * Result structure returned by database initialization
 */
export interface DatabaseInitResult {
  success: boolean
  message?: string
  error?: string
}

/**
 * Result structure returned by Python service start
 */
export interface PythonServiceStartResult {
  success: boolean
  port?: number
  error?: string
}

/**
 * Result structure returned by Python service health check
 */
export interface PythonServiceHealthResult {
  success: boolean
  port?: number
  error?: string
}

/**
 * Result structure returned by Python service get-port
 */
export interface PythonServicePortResult {
  success: boolean
  port?: number
}

/**
 * Python service API
 */
export interface PythonService {
  /**
   * Start the Python ML service
   * @returns Promise resolving to service port
   *
   * @example
   * const result = await window.electronAPI.python.startService()
   * if (result.success) {
   *   console.log('Python service running on port:', result.port)
   * }
   */
  startService(): Promise<PythonServiceStartResult>

  /**
   * Check Python service health
   * @returns Promise resolving to health status
   *
   * @example
   * const result = await window.electronAPI.python.healthCheck()
   * if (result.success) {
   *   console.log('Service is healthy on port:', result.port)
   * }
   */
  healthCheck(): Promise<PythonServiceHealthResult>

  /**
   * Get current Python service port
   * @returns Promise resolving to port number (or null if not started)
   *
   * @example
   * const result = await window.electronAPI.python.getPort()
   * if (result.success && result.port) {
   *   console.log('Service port:', result.port)
   * }
   */
  getPort(): Promise<PythonServicePortResult>
}

/**
 * Electron API exposed to renderer process via contextBridge
 * Provides type-safe database and Python service access through IPC
 */
export interface ElectronAPI {
  /**
   * Execute a SELECT query and return results
   * @param sql - SQL query string with placeholders (?)
   * @param params - Optional parameter array for placeholders
   * @returns Promise resolving to query results array
   *
   * @example
   * const result = await window.electronAPI.queryDatabase(
   *   'SELECT * FROM documents WHERE id = ?',
   *   [documentId]
   * )
   * if (result.success) {
   *   console.log(result.data)
   * }
   */
  queryDatabase: (sql: string, params?: unknown[]) => Promise<DatabaseQueryResult>

  /**
   * Execute an INSERT, UPDATE, or DELETE statement
   * @param sql - SQL statement string with placeholders (?)
   * @param params - Optional parameter array for placeholders
   * @returns Promise resolving to result with lastInsertRowid and changes count
   *
   * @example
   * const result = await window.electronAPI.execDatabase(
   *   'INSERT INTO documents (title, file_path) VALUES (?, ?)',
   *   ['My Document', '/path/to/file.pdf']
   * )
   * if (result.success) {
   *   console.log('Inserted row:', result.lastInsertRowid)
   * }
   */
  execDatabase: (sql: string, params?: unknown[]) => Promise<DatabaseExecResult>

  /**
   * Initialize database schema (create tables if not exist)
   * Called automatically on app startup, but can be called manually if needed
   * @returns Promise resolving to success message
   *
   * @example
   * const result = await window.electronAPI.initDatabase()
   * if (result.success) {
   *   console.log(result.message)
   * }
   */
  initDatabase: () => Promise<DatabaseInitResult>

  /**
   * Python ML service API
   */
  python: PythonService
}

/**
 * Augment global Window interface to include electronAPI
 * This enables TypeScript autocomplete and type checking throughout the app
 */
declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

/**
 * Export empty object to make this a module
 * (Required for global augmentation to work in TypeScript)
 */
export {}
