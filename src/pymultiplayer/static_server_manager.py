from multiprocessing import Process
from .errors import PortInUseError, NoParametersGiven
from json import dumps, loads
import websockets, asyncio
from .health_check import health_check


class StaticServerManager:
    def __init__(self, ip, port, no_of_servers, init_func):
        self.ip = ip
        self.port = port
        self.no_of_servers = no_of_servers
        self.init_func = init_func  # Function ran to initialise a new server

        self.servers = list()
