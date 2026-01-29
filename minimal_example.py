#!/usr/bin/env python3
import asyncio
import websockets

async def handler(websocket):
    while True:
        await websocket.send(f"variable-name={'This can be a string, a number or a boolean.'}")
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
