import websockets, asyncio
from multiprocessing import Process


class TCPMultiplayerServer:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300,):
        self.ip = ip
        self.port = port
        self._msg_handler = msg_handler
        self.clients = []

    async def _run(self, proxy):
        async with websockets.serve(proxy, self.ip, self.port):
            await asyncio.Future()

    async def msg_handler(self, websocket):
        async for msg in websocket:
            await self._msg_handler(msg, websocket)


    def run(self, proxy):
        asyncio.run(self._run(proxy))
