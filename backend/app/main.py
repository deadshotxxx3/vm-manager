from fastapi import FastAPI, HTTPException, WebSocket
from app.qmp import qmp_command, QMPError
from app import vm
from app.terminal import bridge


app = FastAPI(title="vm-manager")


@app.websocket("/ws/serial")
async def serial_ws(websocket):
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


@app.get("/api/vm/status")
async def status():
    try:
        result = await qmp_command("query-status")
        return {"running": True, "status": result["status"]}
    except QMPError:
        return {"running": False, "status": "stopped"}


@app.post("/api/vm/start")
async def start():
    try:
        await vm.start()
    except vm.VMError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"result": "started"}


@app.post("/api/vm/reboot")
async def reboot():
    try:
        await qmp_command("system_reset")
    except QMPError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"result": "rebooting"}


@app.post("/api/vm/stop")
async def stop():
    try:
        await qmp_command("system_powerdown")
    except QMPError as e:
        raise HTTPException(status_code=409,detail=str(e))
    return {"result": "stopping"}