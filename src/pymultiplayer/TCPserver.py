import websockets, asyncio
from ._ws_client import _Client
from .initial_server import InitialServer
from .errors import PortInUseError
from .health_check import health_check
from threading import Thread
from json import dumps, loads


class TCPMultiplayerServer:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_func=None, max_clients=8, sm_port=None, sm_uuid=None, ws_or_wss: str = "ws", start_game_func=None):
        self.ip = ip
        self.port = port
        self.msg_handler = msg_handler
        self.clients = []
        self.last_id = 0
        self.max_clients = max_clients

        self.is_idle = True
        self.sm_port = sm_port
        self.sm_uuid = sm_uuid
        self.ws_or_wss = ws_or_wss
        self.start_game_func = start_game_func

        self.initial_server = InitialServer(self.ip, self.port, auth_func)
        Thread(target=self.initial_server.start).start()

    # Client Communication Functions
    async def broadcast(self, msg):
        for client in self.clients:
            await self.send(client, msg)

    async def send_to_all_except(self, client_not_receiving, msg):
        clients = [client for client in self.clients if client != client_not_receiving]
        for client in clients:
            await self.send(client, msg)

    async def send(self, client, msg):
        try:
           await client.ws.send(msg)
        except websockets.ConnectionClosed:
           self.clients.remove(client)

    # State Management Functions For Use With Static Server Manager
    async def game_finished(self):
        self.is_idle = True
        msg = dumps({"type": "game_complete", "port": self.port})
        async with websockets.connect(f"{self.ws_or_wss}://{self.ip}:{self.sm_port}") as websocket:
            await websocket.send(msg)

    async def _start_game_func(self, parameters):
        self.is_idle = False
        self.start_game_func(parameters)

    # Client Joining/Leaving Functions
    def client_joined_func(self, client):
        pass

    def client_left_func(self, client):
        pass

    def set_client_joined_func(self, func):
        self.client_joined_func = func

    def set_client_left_func(self, func):
        self.client_left_func = func

    # Server Basics (run/proxy)
    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port + 1, process_request=health_check):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get_player_count":
            await websocket.send(dumps({"type": "get_player_count", "content": len(self.clients)}))
            await websocket.close()
            return

        if "uuid" in msg:
            # Request is supposedly from server
            if msg["uuid"] != self.sm_uuid:
                # Request is not legitimate
                msg = {"type": "error", "content": "UUID is invalid."}
                await websocket.send(dumps(msg))
                await websocket.close()
                return

            # Request is legitimately from server
            if msg["type"] == "new_game_parameters":
                await self._start_game_func(msg["content"])

            await websocket.close()
            return

        if self.is_idle:
            await websocket.send(dumps({"type": "error", "content": "Server is not active"}))
            await websocket.close()
            return

        if len(self.clients)+1 > self.max_clients:
            await websocket.send(dumps({"type": "error", "content": "Server is full"}))
            await websocket.close()
            return

        new_client = _Client(websocket, self.last_id + 1)
        self.last_id += 1

        try:
            self.clients.append(new_client)
            await websocket.send(dumps({"type": "id", "content": new_client.id}))

            msg = {"type": "client_joined", "content": new_client.id}
            await self.send_to_all_except(new_client, dumps(msg))

            await self.client_joined_func(new_client)

            while True:
                async for msg_json in websocket:
                    msg = loads(msg_json)
                    await self.msg_handler(msg, new_client)

        finally:
            self.clients.remove(new_client)
            await self.client_left_func(new_client)
            msg = {"type": "client_left", "content": new_client.id}
            await self.broadcast(dumps(msg))
            await websocket.close()

    def run(self):
        asyncio.run(self._run())
