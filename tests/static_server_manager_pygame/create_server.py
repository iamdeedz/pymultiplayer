import websockets
from asyncio import run
from json import dumps, loads


async def main():
    async with websockets.connect(f"wss://pymultiplayer.onrender.com:1300") as websocket:
        await websocket.send(dumps({"type": "create", "parameters": {}}))
        print(loads(await websocket.recv()))
        await websocket.close()


run(main())
