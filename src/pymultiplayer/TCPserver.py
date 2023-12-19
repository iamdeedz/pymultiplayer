import websockets, asyncio
from ._ws_client import _Client
from .errors import PortInUseError
from .initial_server import InitialServer
from .errors import PortInUseError
from threading import Thread
from json import dumps, loads


class TCPMultiplayerServer:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_func=None):
        self.ip = ip
        self.port = port
        self.msg_handler = msg_handler
        self.clients = set()
        self.last_id = 0
        self.initial_server = InitialServer(self.ip, self.port, auth_func)
        Thread(target=self.initial_server.start).start()

    def broadcast(self, msg):
        client_websockets = [client.ws for client in self.clients]
        websockets.broadcast(client_websockets, msg)

    def send_to_all_except(self, client, msg):
        client_websockets = [client.ws for client in self.clients if client != client]
        websockets.broadcast(client_websockets, msg)

    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port + 1):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    async def proxy(self, websocket, path):
        new_client = _Client(websocket, self.last_id + 1)
        self.last_id += 1

        try:
            self.clients.add(new_client)
            await websocket.send(dumps({"type": "id", "content": new_client.id}))

            msg = {"type": "client_joined", "content": new_client.id}
            self.send_to_all_except(new_client, dumps(msg))

            print(f"Client with id {self.last_id} connected")
            async for msg_json in websocket:
                client = [client for client in self.clients if client.ws == websocket][0]
                msg = loads(msg_json)
                await self.msg_handler(msg, client)

        finally:
            self.clients.remove(new_client)
            msg = {"type": "client_left", "content": client.id}
            self.broadcast(dumps(msg))

    def run(self):
        asyncio.run(self._run())
