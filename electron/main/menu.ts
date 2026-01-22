import { app, Menu, shell } from 'electron'

const isMac = process.platform === 'darwin'

export function createMenu() {
  const template: Electron.MenuItemConstructorOptions[] = []

  // App menu (macOS only)
  if (isMac) {
    template.push({
      label: app.name || 'Document Research',
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideOthers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
  }

  // File menu
  template.push({
    label: 'File',
    submenu: [
      isMac ? { role: 'close' } : { role: 'quit' }
    ]
  })

  // Edit menu
  template.push({
    label: 'Edit',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
      { role: 'selectAll' }
    ]
  })

  // View menu
  template.push({
    label: 'View',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
      { type: 'separator' },
      { role: 'togglefullscreen' }
    ]
  })

  // Help menu
  template.push({
    label: 'Help',
    submenu: [
      {
        label: 'Documentation',
        click: () => {
          shell.openExternal('https://github.com/abachman/document-research')
        }
      },
      {
        label: 'Report Issue',
        click: () => {
          shell.openExternal('https://github.com/abachman/document-research/issues')
        }
      }
    ]
  })

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
}
