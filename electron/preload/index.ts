import { contextBridge, ipcRenderer } from 'electron'

/**
 * Electron API exposed to renderer process via contextBridge
 * Provides type-safe database and Python service access through IPC
 */
contextBridge.exposeInMainWorld('electronAPI', {
  /**
   * Execute a SELECT query and return results
   * @param sql - SQL query string with placeholders
   * @param params - Optional parameter array for placeholders
   * @returns Promise resolving to query results array
   */
  queryDatabase: (sql: string, params?: unknown[]) => {
    return ipcRenderer.invoke('db:query', sql, params)
  },

  /**
   * Execute an INSERT, UPDATE, or DELETE statement
   * @param sql - SQL statement string with placeholders
   * @param params - Optional parameter array for placeholders
   * @returns Promise resolving to result with lastInsertRowid and changes count
   */
  execDatabase: (sql: string, params?: unknown[]) => {
    return ipcRenderer.invoke('db:exec', sql, params)
  },

  /**
   * Initialize database schema (create tables if not exist)
   * @returns Promise resolving to success message
   */
  initDatabase: () => {
    return ipcRenderer.invoke('db:init')
  },

  /**
   * Python service API
   */
  python: {
    /**
     * Start the Python ML service
     * @returns Promise resolving to service port
     */
    startService: () => {
      return ipcRenderer.invoke('py:start')
    },

    /**
     * Check Python service health
     * @returns Promise resolving to health status
     */
    healthCheck: () => {
      return ipcRenderer.invoke('py:health')
    },

    /**
     * Get current Python service port
     * @returns Promise resolving to port number (or null if not started)
     */
    getPort: () => {
      return ipcRenderer.invoke('py:get-port')
    }
  }
})
