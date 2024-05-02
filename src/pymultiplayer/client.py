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
                self.id = loads(await websocket.recv())["content"]
                t = Thread(target=self.start_websocket_thread)
                t.start()
                self.event = Event()
                await proxy(websocket)

        except OSError:
            raise ServerUnreachableError(self.ip, self.port)

    """
        if msg["type"] == "error":
            raise ServerError(msg["content"])

        elif msg["type"] == "id":
            self.id = msg["content"]
            print(self.id)

        await self._msg_handler(msg)
        
    """

    def run(self, proxy):
        asyncio.run(self._run(proxy))

    def disconnect(self):
        self.ws.close()

    async def send(self, msg):
        await asyncio.ensure_future(self.ws.send(msg))

    async def websocket_handler(self):
        async for msg in self.ws:
            await self._msg_handler(msg)

        await self.ws.close()
        quit()

    def start_websocket_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.websocket_handler())
