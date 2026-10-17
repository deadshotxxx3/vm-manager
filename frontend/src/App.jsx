import { useState } from 'react'

function App() {
  const [mode, setMode] = useState('serial')

  return (
    <div>
      <h1>VM Manager</h1>
      <button disabled={mode === 'serial'} onClick={() => setMode('serial')}>Serial</button>
      <button disabled={mode === 'ssh'} onClick={() => setMode('ssh')}>SSH</button>
      <p>Режим терминала: {mode}</p>
    </div>
  )
}

export default App