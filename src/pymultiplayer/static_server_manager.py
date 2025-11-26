from multiprocessing import Process
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
from .TCPserver import TCPMultiplayerServer, ServerOptions
from .health_check import health_check
from uuid import uuid4
import websockets, asyncio


class StaticServerManager:
    def __init__(self, no_of_servers, ip="127.0.0.1", port=1300, ws_or_wss: str = "ws"):
        self.ip = ip
        self.port = port
        self.no_of_servers = no_of_servers

        self.uuid = str(uuid4())

        self.ws_or_wss = ws_or_wss

        self.active_servers = list()
        self.idle_servers = list()

        for i in range(self.no_of_servers):
            self.idle_servers.append(self.port+(i*2)+1)

        # all servers always on
        # need a list of idle servers
        # when server is requested, need to first check if there's any servers free
        # then send a message to that server telling it parameters for a new game
        # make sure the server is in the right list
        # send the port of the server to the client

        # SSM -> Server
        # {
        # type; new_game_parameters,
        # content: {level_id: -999, max_players: 4}
        # uuid: sm_uuid
        # }

        # SSM moves server to active_servers list

        # need a way for the server manager to talk to the servers
        # could generate a uuid for the server manager on startup and pass that through to the servers as a parameter
        # then whenever the server manager tries to talk to the servers, it connects, send a message that has the server manager's uuid in it,
        # the server checks if the uuid is correct, then does what the server manager asked.

    async def start_game_server(self, server_port, parameters):
        msg = dumps({"type": "new_game_parameters", "content": parameters, "uuid": self.uuid})
        async with websockets.connect(f"{self.ws_or_wss}://{self.ip}:{server_port+1}") as websocket:
            await websocket.send(msg)
        self.idle_servers.remove(server_port)
        self.active_servers.append({"port": server_port, "parameters": parameters})

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get":
            return_msg = dumps({"type": "get", "content": [server for server in self.active_servers]})
            await websocket.send(return_msg)

        elif msg["type"] == "create":
            if len(self.idle_servers) < 1:
                return_msg = dumps({"type": "create", "status": "error", "content": "all_servers_busy"})
                await websocket.send(return_msg)
                await websocket.close()
                return

            try:
                new_server_port = self.idle_servers[0]
                await self.start_game_server(self.idle_servers[0], msg["parameters"])
                return_msg = dumps({"type": "create", "status": "success", "content": "server_started", "port": new_server_port})
                await websocket.send(return_msg)
                await websocket.close()
            except KeyError:
                return_msg = dumps({"type": "create", "status": "error", "content": "no_parameters_given"})
                await websocket.send(return_msg)
                await websocket.close()
                raise NoParametersGiven()

        elif msg["type"] == "game_complete":
            for server in self.active_servers:
                if server["port"] == msg["port"]:
                    # First message to remove, server sends as many messages as it has clients so only care about the first one.
                    [self.active_servers.remove(server) if server["port"] == msg["port"] else None for server in self.active_servers]
                    self.idle_servers.append(msg["port"])
                    break

    def init_func(self, server_options):
        server = TCPMultiplayerServer(server_options)
        server.run()

    async def run_proxy_with_invalid_msg_except(self, websocket):
        try:
            await self.proxy(websocket)
        except websockets.InvalidMessage as e:
            await self.invalid_msg_error_func(e)
            await websocket.close()

    async def _run(self, server_options):

        server_options.sm_uuid = self.uuid
        server_options.sm_port = self.port
        server_options.is_idle = True
        for port in self.idle_servers:
            print(f"starting server with port {port}")
            # Start all the servers
            server_options.port = port
            process = Process(target=self.init_func, args=(server_options,))
            print("process created")
            process.start()
            print(f"successfully started server with port {port}")

        try:
            # Start the actual server manager
            if server_options.invalid_msg_try_except:
                print("abc")
                self.invalid_msg_error_func = server_options.invalid_msg_error_func
                async with websockets.serve(self.run_proxy_with_invalid_msg_except, self.ip, self.port, process_request=health_check):
                    await asyncio.Future()
            else:
                print("normal ssm")
                async with websockets.serve(self.proxy, self.ip, self.port, process_request=health_check):
                    await asyncio.Future()

        except OSError:
            raise PortInUseError(self.port)

    def run(self, server_options: ServerOptions):
        asyncio.run(self._run(server_options))
