from fastapi import FastAPI, HTTPException

app = FastAPI(title="vm-manager")

@app.get("/api/vm/status")
async def status():
    pass

@app.post("/api/vm/start")
async def start():
    pass

@app.post("/api/vm/reboot")
async def reboot():
    pass

@app.post("/api/vm/stop")
async def stop():
    pass