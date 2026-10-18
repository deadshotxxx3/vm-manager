import { useEffect, useState } from 'react'

const API_URL = '/api/vm'
const POLL_INTERVAL = 2000

async function fetchStatus() {
  try {
    const response = await fetch(`${API_URL}/status`)
    const data = await response.json()
    return data.status
  }
  catch {
    return 'unknown'
  }
}

async function sendCommand(action) {
  try {
    const response = await fetch(`${API_URL}/${action}`, { method: 'POST' })
    if (!response.ok) {
      const data = await response.json()
      return data.detail
    }
    return null
  }
  catch {
    return 'Backend недоступен'
  }
}

function ControlPanel() {
  const [status, setStatus] = useState('unknown')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  async function loadStatus() {
    setStatus(await fetchStatus())
  }

  async function handleClick(action) {
    setBusy(true)
    setError(await sendCommand(action))
    await loadStatus()
    setBusy(false)
  }

  useEffect(() => {
    loadStatus()
    const timer = setInterval(loadStatus, POLL_INTERVAL)
    return () => clearInterval(timer)
  }, [])

  const running = status !== 'stopped' && status !== 'unknown'

  return (
    <div>
      <p>Статус ВМ: {status}</p>
      <button disabled={busy || running} onClick={() => handleClick('start')}>Включить</button>
      <button disabled={busy || !running} onClick={() => handleClick('reboot')}>Перезагрузить</button>
      <button disabled={busy || !running} onClick={() => handleClick('stop')}>Остановить</button>
      {error && <p>Ошибка: {error}</p>}
    </div>
  )
}

export default ControlPanel
