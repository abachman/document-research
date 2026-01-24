import { spawn, ChildProcess } from 'child_process'
import { readFileSync, existsSync } from 'fs'
import { join } from 'path'
import { app } from 'electron'
import { EventEmitter } from 'events'

/** Constants for Python service management */
const PORT_POLL_INTERVAL = 100 // ms
const MAX_STARTUP_TIME = 5000 // ms (50 attempts)
const MAX_AUTO_RESTART = 3 // times
const PORT_FILE_NAME = 'doc-research-ml-port.txt'

/**
 * PythonServiceManager manages the lifecycle of the Python ML service.
 * Handles spawning, health checking, auto-restart on crash, and port discovery.
 */
class PythonServiceManager extends EventEmitter {
  private process: ChildProcess | null = null
  private port: number | null = null
  private restartCount = 0
  private isStarting = false
  private startPromise: Promise<number> | null = null

  constructor() {
    super()
  }

  /**
   * Get the Python executable path based on environment
   * @returns Path to Python interpreter
   */
  private getPythonPath(): string {
    if (app.isPackaged) {
      // Production: Use bundled Python runtime
      return join(process.resourcesPath, 'python-runtime', 'bin', 'python3')
    }
    // Development: Use system Python
    return 'python3'
  }

  /**
   * Get the main.py script path based on environment
   * @returns Path to Python service main script
   */
  private getScriptPath(): string {
    if (app.isPackaged) {
      return join(process.resourcesPath, 'python-service', 'main.py')
    }
    // Development: Use relative path from compiled JS
    return join(__dirname, '../../python-service/main.py')
  }

  /**
   * Get the port file path in the temp directory
   * @returns Path to port file
   */
  private getPortFilePath(): string {
    const tempDir = app.getPath('temp')
    return join(tempDir, PORT_FILE_NAME)
  }

  /**
   * Wait for the port file to be created by Python service
   * Polls every 100ms with 5 second timeout
   * @returns Port number from file
   * @throws Error if timeout occurs
   */
  private async waitForPortFile(): Promise<number> {
    const portFilePath = this.getPortFilePath()

    for (let attempt = 0; attempt < MAX_STARTUP_TIME / PORT_POLL_INTERVAL; attempt++) {
      if (existsSync(portFilePath)) {
        const portContent = readFileSync(portFilePath, 'utf-8').trim()
        const port = parseInt(portContent, 10)
        if (!isNaN(port)) {
          console.log(`[PythonService] Port file found: ${port}`)
          return port
        }
      }
      // Wait before next poll
      await new Promise(resolve => setTimeout(resolve, PORT_POLL_INTERVAL))
    }

    throw new Error(`Python service startup timeout: Port file not created after ${MAX_STARTUP_TIME}ms`)
  }

  /**
   * Perform health check on Python service
   * @returns true if service is healthy, false otherwise
   */
  async healthCheck(): Promise<boolean> {
    if (!this.port) {
      return false
    }

    try {
      const response = await fetch(`http://127.0.0.1:${this.port}/health`)
      return response.ok
    } catch (error) {
      console.warn('[PythonService] Health check failed:', error)
      return false
    }
  }

  /**
   * Start the Python service
   * @returns Port number of the running service
   */
  async startPythonService(): Promise<number> {
    // Return existing promise if already starting
    if (this.isStarting && this.startPromise) {
      return this.startPromise
    }

    // If already running, check health and return port
    if (this.port) {
      const isHealthy = await this.healthCheck()
      if (isHealthy) {
        console.log(`[PythonService] Already running on port ${this.port}`)
        return this.port
      }
      // Not healthy, reset and restart
      console.warn('[PythonService] Existing service unhealthy, restarting...')
      this.port = null
    }

    // Create start promise
    this.startPromise = this.doStart()

    try {
      const port = await this.startPromise
      return port
    } finally {
      this.startPromise = null
    }
  }

  /**
   * Internal method to spawn Python process and wait for port
   */
  private async doStart(): Promise<number> {
    this.isStarting = true

    try {
      const pythonPath = this.getPythonPath()
      const scriptPath = this.getScriptPath()

      console.log(`[PythonService] Starting: ${pythonPath} ${scriptPath}`)

      // Spawn Python process
      this.process = spawn(pythonPath, [scriptPath], {
        env: {
          ...process.env,
          PYTHONUNBUFFERED: '1'
        },
        detached: false
      })

      // Handle stderr for error logging
      this.process.stderr?.on('data', (data) => {
        console.error(`[PythonService stderr]: ${data}`)
      })

      // Handle stdout for info logging
      this.process.stdout?.on('data', (data) => {
        console.log(`[PythonService stdout]: ${data}`)
      })

      // Handle process exit (crash or normal shutdown)
      this.process.on('exit', (code, signal) => {
        console.log(`[PythonService] Process exited (code: ${code}, signal: ${signal})`)
        this.process = null

        if (signal === 'SIGTERM' || signal === 'SIGINT') {
          // Intentional shutdown
          console.log('[PythonService] Graceful shutdown complete')
          return
        }

        // Crash detected
        this.restartCount++
        console.warn(`[PythonService] Crash detected (restart ${this.restartCount}/${MAX_AUTO_RESTART})`)

        if (this.restartCount <= MAX_AUTO_RESTART) {
          console.log('[PythonService] Auto-restarting...')
          setTimeout(() => {
            this.startPythonService().catch(err => {
              console.error('[PythonService] Auto-restart failed:', err)
            })
          }, 1000)
        } else {
          console.error('[PythonService] Max restarts reached, giving up')
          this.emit('error', new Error('Python service crashed too many times'))
        }
      })

      // Wait for port file
      const port = await this.waitForPortFile()
      this.port = port
      this.isStarting = false
      this.restartCount = 0 // Reset on successful start

      console.log(`[PythonService] Started successfully on port ${port}`)
      this.emit('started', port)

      return port
    } catch (error) {
      this.isStarting = false
      throw error
    }
  }

  /**
   * Get the current port (if service is running)
   * @returns Port number or null if not running
   */
  getPort(): number | null {
    return this.port
  }
}

// Singleton instance
export const pythonServiceManager = new PythonServiceManager()

/**
 * Convenience function to start Python service
 * @returns Port number of the running service
 */
export async function startPythonService(): Promise<number> {
  return pythonServiceManager.startPythonService()
}

/**
 * Convenience function to get current port
 * @returns Port number or null if not running
 */
export function getPythonServicePort(): number | null {
  return pythonServiceManager.getPort()
}
