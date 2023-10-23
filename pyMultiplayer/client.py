import websockets, asyncio


class MultiplayerClient:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self._msg_handler = msg_handler

    async def _run(self, proxy):
        async with websockets.connect(f"ws://{self.ip}:{self.port}") as websocket:
            uri = await websocket.recv()
            await websocket.close()

        async with websockets.connect(uri) as websocket:
            await proxy(websocket)

    async def msg_handler(self, websocket):
        async for msg in websocket:
            await self._msg_handler(msg, websocket)

    def run(self, proxy):
        asyncio.run(self._run(proxy))
