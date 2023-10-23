import websockets, asyncio
from threading import Thread


class InitialServer:
    def __init__(self, ip="127.0.0.1", port=1300, auth_func=None):
        self.ip = ip
        self.port = port
        self._auth_func = auth_func

    async def _start(self):
        async with websockets.serve(self.new_client, self.ip, self.port):
            await asyncio.Future()

    async def new_client(self, websocket):
        if self._auth_func:
            await self._auth_func(websocket)
        await websocket.send(f"ws://{self.ip}:{self.port + 1}")
        await websocket.close()

    def start(self):
        asyncio.run(self._start())
