import websockets, asyncio, json
from multiprocessing import Process


class TCPMultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None
        self.clients = []

    async def _run(self, proxy):
        async with websockets.serve(proxy, self.ip, self.port):
            await asyncio.Future()

    def run(self, proxy):
        asyncio.run(self._run(proxy))
