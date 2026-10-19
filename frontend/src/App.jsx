import { useState } from 'react'
import ControlPanel from './ControlPanel'
import Terminal from './Terminal'

function App() {
  const [mode, setMode] = useState('serial')
  const [session, setSession] = useState(0)

  return (
    <div>
      <h1>VM Manager</h1>
      <ControlPanel />
      <div>
        <button disabled={mode === 'serial'} onClick={() => setMode('serial')}>Serial</button>
        <button disabled={mode === 'ssh'} onClick={() => setMode('ssh')}>SSH</button>
        <button onClick={() => setSession(session + 1)}>Переподключить</button>
      </div>
      <Terminal key={session} mode={mode} />
    </div>
  )
}

export default App
