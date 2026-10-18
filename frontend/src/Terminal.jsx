import { useEffect, useRef } from 'react'
import { Terminal as XTerm } from '@xterm/xterm'
import '@xterm/xterm/css/xterm.css'

const WS_URL = `ws://${location.host}/ws`
const TERM_COLS = 80
const TERM_ROWS = 24

function Terminal({ mode }) {
  const containerRef = useRef(null)

  useEffect(() => {
    const term = new XTerm({ cols: TERM_COLS, rows: TERM_ROWS, cursorBlink: true })
    term.open(containerRef.current)

    const ws = new WebSocket(`${WS_URL}/${mode}`)
    ws.binaryType = 'arraybuffer'

    ws.onopen = () => {
      term.write(`[подключено: ${mode}]\r\n`)
      if (mode === 'serial') {
        ws.send('\r')
      }
    }

    ws.onmessage = (event) => {
      term.write(new Uint8Array(event.data))
    }

    ws.onclose = (event) => {
      term.write(`\r\n[соединение закрыто: ${event.code} ${event.reason}]\r\n`)
    }

    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data)
      }
    })

    term.focus()

    return () => {
      ws.onclose = null
      ws.close()
      term.dispose()
    }
  }, [mode])

  return <div ref={containerRef} />
}

export default Terminal
