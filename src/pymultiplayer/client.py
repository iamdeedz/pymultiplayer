import websockets, asyncio
from .errors import ServerError, ServerClosedError, ServerUnreachableError
from json import dumps, loads


class MultiplayerClient:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_handler=None):
        self.ip = ip
        self.port = port
        self.ws = None
        self.id = None
        self._msg_handler = msg_handler
        self._auth_handler = auth_handler

    async def _run(self, proxy):
        try:
            async with websockets.connect(f"ws://{self.ip}:{self.port}") as websocket:
                if self._auth_handler:
                    await self._auth_handler(websocket)

                msg = await websocket.recv()
                uri = loads(msg)["content"]
                if not uri.startswith("ws://"):
                    print("Invalid URI")
                    await websocket.close()
                    quit()

                await websocket.close()

            async with websockets.connect(uri) as websocket:
                self.ws = websocket
                websocket.send(dumps({"type": "greeting"}))
                await proxy(websocket)

        except OSError:
            raise ServerUnreachableError(self.ip, self.port)

    async def msg_handler(self):
        try:
            async for msg_json in self.ws:
                msg = loads(msg_json)
                if msg["type"] == "error":
                    raise ServerError(msg["content"])

                elif msg["type"] == "id":
                    self.id = msg["content"]
                    print(self.id)

                await self._msg_handler(msg)
        
        except websockets.exceptions.ConnectionClosedError:
            raise ServerClosedError()

    def run(self, proxy):
        asyncio.run(self._run(proxy))
