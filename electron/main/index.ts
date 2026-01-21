import { app, BrowserWindow } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'
import electronServe from 'electron-serve'

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

  if (app.isPackaged) {
    // Production: Load static Next.js export
    appServe(win).then(() => {
      win.loadURL('app://-')
    })
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
