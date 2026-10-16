import asyncio
from fastapi import WebSocketDisconnect


async def browser_to_vm(websocket, writer):
    try:
        while True:
            text = await websocket.receive_text()
            writer.write(text.encode())
            await writer.drain()
    except WebSocketDisconnect:
        pass


async def vm_to_browser(reader, websocket):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        await websocket.send_bytes(data)
    await websocket.close()


async def bridge(websocket, reader, writer):
    task1 = asyncio.create_task(browser_to_vm(websocket, writer))
    task2 = asyncio.create_task(vm_to_browser(reader, websocket))
    await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
    task1.cancel()
    task2.cancel()