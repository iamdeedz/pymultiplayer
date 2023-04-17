import asyncio
import websockets


async def proxy(websocket):
    pass


async def main():
    async with websockets.serve(proxy, "localhost", 4031):
        print("Hosting server at localhost:4031")
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
