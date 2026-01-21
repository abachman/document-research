import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  // IPC invoke (request-response) - will be used in 01-05
  sendMessage: (channel: string, data: unknown) => {
    return ipcRenderer.invoke(channel, data)
  },
  // IPC send (fire-and-forget) - will be used in 01-05
  send: (channel: string, data: unknown) => {
    ipcRenderer.send(channel, data)
  },
  // IPC on (listen to messages from main) - will be used in 01-05
  on: (channel: string, callback: (...args: unknown[]) => void) => {
    ipcRenderer.on(channel, (event, ...args) => callback(...args))
  },
  // Remove listener - will be used in 01-05
  removeAllListeners: (channel: string) => {
    ipcRenderer.removeAllListeners(channel)
  }
})
