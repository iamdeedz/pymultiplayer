import websockets, asyncio
from ._ws_client import _Client
from .initial_server import InitialServer
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

    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port + 1):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    async def proxy(self, websocket, path):
        client = _Client(websocket, self.last_id + 1)
        self.last_id += 1

        try:
            self.clients.add(client)
            for client in self.clients:
                if client.ws == websocket:
                    continue
                msg = {"type": "client_joined", "content": client.id}
                await client.ws.send(dumps(msg))
            print(f"Client with id {self.last_id} connected")
            async for msg_json in websocket:
                client = [client for client in self.clients if client.ws == websocket][0]
                msg = loads(msg_json)
                await self.msg_handler(msg, client)

        finally:
            self.clients.remove(client)
            msg = {"type": "client_left", "content": client.id}
            self.broadcast(dumps(msg))


    def run(self):
        asyncio.run(self._run())
