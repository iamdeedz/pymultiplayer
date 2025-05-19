import websockets, asyncio
from .errors import ServerError, ServerClosedError, ServerUnreachableError
from json import loads, dumps
from threading import Thread, Event


class MultiplayerClient:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_handler=None, ws_or_wss: str = "ws"):
        self.ip = ip
        self.port = port
        self.ws = None
        self.id = None
        self.ws_thread = None
        self.ws_or_wss = ws_or_wss
        self._msg_handler = msg_handler
        self._auth_handler = auth_handler

    async def websocket_handler(self):
        try:
            async with websockets.connect(f"{self.ws_or_wss}://{self.ip}:{self.port}") as websocket:
                if self._auth_handler:
                    await self._auth_handler(websocket)

                msg = await websocket.recv()
                uri = loads(msg)["content"]
                if not uri.startswith(f"{self.ws_or_wss}://"):
                    print("Invalid URI")
                    await websocket.close()
                    quit()

                await websocket.close()

            async with websockets.connect(uri) as websocket:
                self.ws = websocket

                # This message tells the server to continue processing this client as if they want to join (which they do)
                # instead of returning the amount of players connected to the server
                await self.ws.send(dumps({"type": ""}))

                self.id = loads(await websocket.recv())["content"]

                async for msg in self.ws:
                    await self._msg_handler(msg)

                await self.disconnect()
                quit()

        except OSError:
            raise ServerUnreachableError(self.ip, self.port)

    def start(self):
        self.ws_thread = Thread(target=self.start_websocket_thread)
        self.ws_thread.start()

    async def disconnect(self):
        await self.ws_thread.join()
        await self.ws.close()

    async def send(self, msg):
        await asyncio.ensure_future(self.ws.send(msg))

    def start_websocket_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.websocket_handler())
