import websockets
from asyncio import run
from json import dumps, loads


async def main():
    async with websockets.connect(f"ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "create", "parameters": ()}))
        print(loads(await websocket.recv()))
        await websocket.close()


run(main())
