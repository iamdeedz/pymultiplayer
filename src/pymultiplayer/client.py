import websockets, asyncio
from .errors import ServerError, ServerClosedError, ServerUnreachableError
from json import loads
from threading import Thread, Event


class MultiplayerClient:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_handler=None):
        self.ip = ip
        self.port = port
        self.ws = None
        self.id = None
        self.event = None
        self._msg_handler = msg_handler
        self._auth_handler = auth_handler

    async def websocket_handler(self):
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
                self.id = loads(await websocket.recv())["content"]
                async for msg in self.ws:
                    await self._msg_handler(msg)

                await self.ws.close()
                quit()

        except OSError:
            raise ServerUnreachableError(self.ip, self.port)

    def start(self):
        t = Thread(target=self.start_websocket_thread)
        t.start()

    async def disconnect(self):
        await self.ws.close()

    async def send(self, msg):
        await asyncio.ensure_future(self.ws.send(msg))

    def start_websocket_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.websocket_handler())
