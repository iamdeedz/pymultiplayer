import socket
from threading import Thread


class UDPMultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
