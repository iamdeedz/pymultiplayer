import websockets, asyncio
from .errors import PortInUseError, AuthServerOffline
from json import dumps
from .health_check import health_check


class InitialServer:
    def __init__(self, ip="127.0.0.1", port=1300, auth_func=None, ws_or_wss: str = "ws"):
        self.ip = ip
        self.port = port
        self.ws_or_wss = ws_or_wss
        self._auth_func = auth_func

    async def _start(self):
        try:
            async with websockets.serve(self.new_client, self.ip, self.port, process_request=health_check):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    async def new_client(self, websocket):
        if self._auth_func:
            try:
                await self._auth_func(websocket)
            except OSError:
                msg = {"type": "error", "content": "Server encountered an OSError during the authorization process."}
                await websocket.send(dumps(msg))
                await websocket.close()
                raise AuthServerOffline()

        msg = {"type": "uri", "content": f"{self.ws_or_wss}://{self.ip}:{self.port + 1}"}
        await websocket.send(dumps(msg))
        await websocket.close()

    def start(self):
        asyncio.run(self._start())
