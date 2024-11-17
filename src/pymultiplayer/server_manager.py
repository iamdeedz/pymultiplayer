from threading import Thread
from .TCPserver import TCPMultiplayerServer
from .errors import PortInUseError
from json import dumps, loads
import websockets, asyncio


class Server:
    def __init__(self, port, name):
        self.port = port
        self.name = name

    def __repr__(self):
        return f"{self.name} @ {self.port}"


class ServerManager:
    def __init__(self, ip, port, max_servers):
        self.ip = ip
        self.port = port
        self.max_servers = max_servers
        self.servers = list()
        self.servers.append(Server(1301, "test 1"))
        self.servers.append(Server(1303, "test 2"))

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get":
            return_msg = dumps({"type": "get", "servers": self.servers})
            await websocket.send(return_msg)

    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    def run(self):
        asyncio.run(self._run())

# { "type": "get/create", -if create then- "" }


server_manager = ServerManager("127.0.0.1", 1300, 2)
server_manager.run()
