import websockets
import asyncio


async def main():
    uri = "ws://127.0.0.1:1300"
    async with websockets.connect(uri) as websocket:
        print("Connected")
        msg = "Hello world!"
        print(f'Sending "{msg}" to server...')
        await websocket.send(msg)
        print(f'server sent "{await websocket.recv()}"')


asyncio.run(main())