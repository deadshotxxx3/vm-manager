import asyncio

from fastapi import WebSocketDisconnect

CNT_BIT_TO_READ = 1024


async def browser_to_vm(websocket, writer) -> None:
    try:
        while True:
            text = await websocket.receive_text()
            writer.write(text.encode())
            await writer.drain()
    except WebSocketDisconnect:
        pass


async def vm_to_browser(reader, websocket) -> None:
    while True:
        data = await reader.read(CNT_BIT_TO_READ)
        if not data:
            break
        await websocket.send_bytes(data)
    await websocket.close()


async def bridge(websocket, reader, writer) -> None:
    task1 = asyncio.create_task(browser_to_vm(websocket, writer))
    task2 = asyncio.create_task(vm_to_browser(reader, websocket))
    await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
    task1.cancel()
    task2.cancel()
