from multiprocessing import Process
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
from .health_check import health_check
from uuid import uuid4
import websockets, asyncio


class StaticServerManager:
    def __init__(self, ip, port, no_of_servers, init_func):
        self.ip = ip
        self.port = port
        self.no_of_servers = no_of_servers
        self.init_func = init_func  # Function ran to initialise a new server

        self.uuid = uuid4()

        self.busy_servers = list()
        self.idle_servers = list()

        for i in range(self.no_of_servers):
            self.idle_servers.append(self.port+(i*2)+1)

        # all servers always on
        # need a list of idle servers
        # when server is requested, need to first check if there's any servers free
        # then send a message to that server telling it to expect a client
        # make sure the server is in the right list
        # send the port of the server to the client

        # need a way for the server manager to talk to the servers
        # could generate a uuid for the server manager on startup and pass that through to the servers as a parameter
        # then whenever the server manager tries to talk to the servers, it connects, send a message that has the server manager's uuid in it,
        # the server checks if the uuid is correct, then does what the server manager asked.

    async def send_message_to_server(self, server_port):
        msg = dumps({"type": "test", "content": "test", "uuid": self.uuid})

    async def proxy(self, websocket):
        msg = loads(await websocket.recv())
        if msg["type"] == "get":
            return_msg = dumps({"type": "get", "content": [server for server in self.busy_servers]})
            await websocket.send(return_msg)

        elif msg["type"] == "create":
            if len(self.idle_servers) < 1:
                return_msg = dumps({"type": "create", "status": "error", "content": "all_servers_busy"})
                await websocket.send(return_msg)


