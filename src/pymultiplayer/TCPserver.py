import websockets, asyncio
from ._ws_client import _Client
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
        print("Broadcasting")
        websockets.broadcast(client_websockets, msg)
        print("Broadcasted")

    def send_to_all_except(self, client, msg):
        client_websockets = [client.ws for client in self.clients if client != client]
        print("Sending to all except", client.id)
        websockets.broadcast(client_websockets, msg)
        print("Sent to all except", client.id)

    def send_to(self, client, msg):
        client.ws.send(msg)

    def client_joined_func(self, client):
        pass

    def client_left_func(self, client):
        pass

    def set_client_joined_func(self, func):
        self.client_joined_func = func

    def set_client_left_func(self, func):
        self.client_left_func = func

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

            self.client_joined_func(new_client)

            print("Waiting for messages")
            async for msg_json in websocket:
                print("Message received")
                msg = loads(msg_json)
                self.msg_handler(msg, new_client.id)
                print("Message handled")

        finally:
            self.clients.remove(new_client)
            self.client_left_func(new_client)
            msg = {"type": "client_left", "content": new_client.id}
            self.broadcast(dumps(msg))
            await websocket.close()

    def run(self):
        asyncio.run(self._run())
