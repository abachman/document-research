import { ipcMain } from 'electron'
import { pythonServiceManager, startPythonService } from '../python-service.js'

/**
 * Register IPC handlers for Python service operations
 * Follows structured response pattern: {success, ...data}
 */
export function registerHandlers(): void {
  // Handler: py:start - Start Python service and return port
  ipcMain.handle('py:start', async () => {
    try {
      const port = await startPythonService()
      return {
        success: true,
        port
      }
    } catch (error) {
      console.error('[IPC] py:start error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  })

  // Handler: py:health - Check if Python service is healthy
  ipcMain.handle('py:health', async () => {
    try {
      const port = pythonServiceManager.getPort()

      if (!port) {
        return {
          success: false,
          error: 'Service not started'
        }
      }

      const isHealthy = await pythonServiceManager.healthCheck()

      return {
        success: isHealthy,
        port
      }
    } catch (error) {
      console.error('[IPC] py:health error:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }
    }
  })

  // Handler: py:get-port - Get current port without starting service
  ipcMain.handle('py:get-port', async () => {
    const port = pythonServiceManager.getPort()
    return {
      success: true,
      port
    }
  })

  console.log('[IPC] Python service handlers registered')
}
