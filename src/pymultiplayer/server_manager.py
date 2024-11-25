from threading import Thread
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
import websockets, asyncio


class ServerManager:
    def __init__(self, ip, port, max_servers, init_func):
        self.ip = ip
        self.port = port
        self.max_servers = max_servers
        self.init_func = init_func  # Function ran to initialise a new server

        self.servers = list()

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get":
            return_msg = dumps({"type": "get", "content": self.servers})
            await websocket.send(return_msg)

        elif msg["type"] == "create":
            if len(self.servers)+1 <= self.max_servers:

                try:
                    new_server_port = self.port+1 + (len(self.servers)*2)
                    t = Thread(target=self.init_func, args=(self.ip, new_server_port, msg["parameters"],))
                    t.start()
                    self.servers.append(new_server_port)
                    return_msg = dumps({"type": "create", "status": "success", "content": "thread_started"})
                    await websocket.send(return_msg)
                    await websocket.close()

                except KeyError:
                    return_msg = dumps({"type": "create", "status": "error", "content": "no_parameters_given"})
                    await websocket.send(return_msg)
                    await websocket.close()
                    raise NoParametersGiven()

            else:
                return_msg = dumps({"type": "create", "status": "error", "content": "max_server_limit_reached"})
                await websocket.send(return_msg)
                await websocket.close()

    async def _run(self):
        try:
            async with websockets.serve(self.proxy, self.ip, self.port):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    def run(self):
        asyncio.run(self._run())


async def get_servers(ip, port):
    async with websockets.connect(f"ws://{ip}:{port}") as websocket:
        await websocket.send(dumps({"type": "get"}))
        return_msg = loads(await websocket.recv())
        await websocket.close()
        return return_msg

