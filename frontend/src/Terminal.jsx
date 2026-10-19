import { useEffect, useRef } from 'react'
import { Terminal as XTerm } from '@xterm/xterm'
import '@xterm/xterm/css/xterm.css'

const WS_URL = `ws://${location.host}/ws`
const TERM_COLS = 80
const TERM_ROWS = 24

const GREEN = '\x1b[32m'
const RED = '\x1b[31m'
const RESET = '\x1b[0m'

function Terminal({ mode }) {
  const containerRef = useRef(null)

  useEffect(() => {
    const term = new XTerm({ cols: TERM_COLS, rows: TERM_ROWS, cursorBlink: true })
    term.open(containerRef.current)

    const ws = new WebSocket(`${WS_URL}/${mode}`)
    ws.binaryType = 'arraybuffer'

    ws.onopen = () => {
      term.write(`${GREEN}[подключено: ${mode}]${RESET}\r\n`)
      if (mode === 'serial') {
        ws.send('\r')
      }
    }

    ws.onmessage = (event) => {
      term.write(new Uint8Array(event.data))
    }

    ws.onclose = (event) => {
      term.write(`\r\n${RED}[соединение закрыто: ${event.code} ${event.reason}]${RESET}\r\n`)
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
