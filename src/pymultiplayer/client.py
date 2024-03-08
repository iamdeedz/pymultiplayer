import websockets, asyncio
from .errors import ServerError, ServerClosedError, ServerUnreachableError
from json import loads
from threading import Thread

msg_list = []


async def add_msgs_to_list(ws):
    global msg_list
    async for msg_json in ws:
        msg_list.append(loads(msg_json))


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
                self.id = loads(await websocket.recv())["content"]
                thread = Thread(target=asyncio.run, args=(add_msgs_to_list(websocket),))
                thread.start()
                await proxy(websocket)

        except OSError:
            raise ServerUnreachableError(self.ip, self.port)

    async def handle_msgs(self):
        for msg in msg_list:
            await self.handle_msg(msg)

    async def handle_msg(self, msg):
        global msg_list
        msg_list.remove(msg)

        if msg["type"] == "error":
            raise ServerError(msg["content"])

        elif msg["type"] == "id":
            self.id = msg["content"]
            print(self.id)

        await self._msg_handler(msg)

    def run(self, proxy):
        asyncio.run(self._run(proxy))

    def disconnect(self):
        self.ws.close()

    async def send(self, msg):
        await self.ws.send(msg)
