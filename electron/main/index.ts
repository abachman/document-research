import { app, BrowserWindow } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'
import electronServe from 'electron-serve'
import { registerHandlers } from './ipc/handlers.js'
import { registerHandlers as registerPythonHandlers } from './ipc/python.js'
import { createMenu } from './menu.js'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

const appServe = app.isPackaged
  ? electronServe({ directory: join(__dirname, '../../out') })
  : null

const createWindow = () => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false // Set to true for production security
    }
  })

  if (app.isPackaged && appServe) {
    // Production: Load static Next.js export
    appServe(win).then(() => {
      win.loadURL('app://-')
    })
  } else if (app.isPackaged && !appServe) {
    throw new Error('App is packaged but electron-serve is not configured.')
  } else {
    // Development: Load Next.js dev server
    win.loadURL('http://localhost:3000')
    win.webContents.openDevTools()

    // Handle case where Electron starts before Next.js
    win.webContents.on('did-fail-load', () => {
      win.webContents.reloadIgnoringCache()
    })
  }
}

app.whenReady().then(() => {
  createMenu()
  registerHandlers()
  registerPythonHandlers()
  createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
