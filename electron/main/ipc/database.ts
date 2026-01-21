import Database from 'better-sqlite3'
import { app } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

// Initialize SQLite database at userData path
const dbPath = join(app.getPath('userData'), 'annotations.db')
export const db = new Database(dbPath)

// Enable foreign keys
db.pragma('foreign_keys = ON')

/**
 * Initialize database schema with annotations and documents tables
 */
export function initializeSchema(): void {
  // Create annotations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS annotations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      type TEXT NOT NULL CHECK(type IN ('highlight', 'note')),
      text TEXT NOT NULL,
      position TEXT NOT NULL,
      note TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `)

  // Create documents table (for Phase 3)
  db.exec(`
    CREATE TABLE IF NOT EXISTS documents (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      filename TEXT NOT NULL,
      filepath TEXT NOT NULL UNIQUE,
      title TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `)

  // Create indexes for better query performance
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_annotations_type ON annotations(type);
    CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
  `)
}

// Close database connection on app quit
app.on('before-quit', () => {
  db.close()
})
