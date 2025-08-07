from multiprocessing import Process
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
from .TCPserver import TCPMultiplayerServer
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
        self.active_servers.append(server_port)

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
                await self.start_game_server(self.idle_servers[0], msg["parameters"])
            except KeyError:
                return_msg = dumps({"type": "create", "status": "error", "content": "no_parameters_given"})
                await websocket.send(return_msg)
                await websocket.close()
                raise NoParametersGiven()

    def init_func(self, ip, port, sm_uuid, msg_handler, client_joined_func, client_left_func, start_game_func):
        server = TCPMultiplayerServer(msg_handler, ip, port, sm_port=self.port, sm_uuid=sm_uuid, start_game_func=start_game_func)
        if client_joined_func:
            server.set_client_joined_func(client_joined_func)
        if client_left_func:
            server.set_client_left_func(client_left_func)
        server.run()

    async def _run(self, msg_handler, client_joined_func, client_left_func, start_game_func):

        for port in self.idle_servers:
            # Start all the servers
            process = Process(target=self.init_func, args=(self.ip, port, self.uuid, msg_handler, client_joined_func, client_left_func, start_game_func,))
            process.start()

        try:
            # Start the actual server manager
            async with websockets.serve(self.proxy, self.ip, self.port, process_request=health_check):
                await asyncio.Future()

        except OSError:
            raise PortInUseError(self.port)

    def run(self, msg_handler, client_joined_func=None, client_left_func=None, start_game_func=None):
        asyncio.run(self._run(msg_handler, client_joined_func, client_left_func, start_game_func))
