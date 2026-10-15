from fastapi import FastAPI, HTTPException
from app.qmp import qmp_command, QMPError
from app import vm


app = FastAPI(title="vm-manager")


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