'use client';

export default function IPCTest() {
  const testIPC = async () => {
    try {
      await window.electronAPI.initDatabase();
      console.log('Database initialized');

      await window.electronAPI.execDatabase(
        'INSERT INTO annotations (type, text, position) VALUES (?, ?, ?)',
        ['highlight', 'Test text', '{"page": 1}']
      );
      console.log('Insert successful');

      const results = await window.electronAPI.queryDatabase('SELECT * FROM annotations');
      console.log('Query results:', results);
    } catch (error) {
      console.error('IPC error:', error);
    }
  };

  return (
    <div className="p-4">
      <h1>IPC Bridge Test</h1>
      <button onClick={testIPC}>Test IPC</button>
    </div>
  );
}
