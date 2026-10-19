
import asyncio
from pathlib import Path

import asyncssh
from app import vm
from app.qmp import QMPError, qmp_command
from app.terminal import bridge
from fastapi import FastAPI, HTTPException, WebSocket

# serial
SERIAL_SOCK = "/tmp/serial.sock"

# ssh ключ
SSH_HOST = "127.0.0.1"
SSH_PORT = 2222
SSH_USER = "debian"
SSH_KEY = Path(__file__).resolve().parents[2] / "image" / "keys" / "ssh_key"
SSH_TIMEOUT = 10

# терминал
TERM_TYPE = "xterm-256color"
TERM_COLS = 80
TERM_ROWS = 24


app = FastAPI(title="vm-manager")


@app.websocket("/ws/serial")
async def serial_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        reader, writer = await asyncio.open_unix_connection(SERIAL_SOCK)
    except (FileNotFoundError, ConnectionRefusedError):
        await websocket.close(code=1011, reason="VM is not running")
        return

    try:
        await bridge(websocket, reader, writer)
    finally:
        writer.close()


@app.websocket("/ws/ssh")
async def ssh_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        conn = await asyncssh.connect(
            SSH_HOST,
            port=SSH_PORT,
            username=SSH_USER,
            client_keys=[str(SSH_KEY)],
            known_hosts=None,
            connect_timeout=SSH_TIMEOUT,
        )
    except (OSError, asyncssh.Error):
        await websocket.close(code=1011, reason="SSH connection failed")
        return
    try:
        process = await conn.create_process(
            term_type=TERM_TYPE,
            term_size=(TERM_COLS, TERM_ROWS),
            encoding=None,
        )
        await bridge(websocket, process.stdout, process.stdin)
    finally:
        conn.close()


@app.get("/api/vm/status")
async def status() -> dict:
    try:
        result = await qmp_command("query-status")
        return {"running": True, "status": result["status"]}
    except QMPError:
        return {"running": False, "status": "stopped"}


@app.post("/api/vm/start")
async def start() -> dict[str, str]:
    try:
        await vm.start()
    except vm.VMError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"result": "started"}


@app.post("/api/vm/reboot")
async def reboot() -> dict[str, str]:
    try:
        await qmp_command("system_reset")
    except QMPError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"result": "rebooting"}


@app.post("/api/vm/stop")
async def stop() -> dict[str, str]:
    try:
        await qmp_command("system_powerdown")
    except QMPError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"result": "stopping"}
