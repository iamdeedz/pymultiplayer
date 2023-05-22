from websocket_server import WebsocketServer
from re import match
from .errors import *
import websocket
import socket


class MultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300, protocol="TCP"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.clients = []
        self.initial_server = None
        self.server = None
        self.start()

    def start(self):
        if self.protocol != "TCP" and self.protocol != "UDP":
            raise InvalidProtocolError(self.protocol)
        self.start_initial_server()
        self.start_main_server()

    def start_initial_server(self):
        try:
            self.initial_server = WebsocketServer(host=self.ip, port=self.port)
        except OSError:
            raise PortInUseError(self.port)
        self.initial_server.set_fn_new_client(self.initial_server_new_client)
        self.initial_server.run_forever(threaded=True)

    def initial_server_new_client(self, client, server):
        print(f"Client with id {client['id']} connected.")
        self.send_to_main_server()

    def main_server_new_client(self, client, server):
        print(f"Client with id {client['id']} connected.")

    def send_to_main_server(self):
        if self.protocol == "TCP":
            self.initial_server.send_message_to_all(f"ws://{self.ip}:{self.port + 1}")
        elif self.protocol == "UDP":
            self.initial_server.send_message_to_all(f"{self.ip}:{self.port + 1}")

    def start_main_server(self):
        if self.protocol == "TCP":

            try:
                self.server = WebsocketServer(host=self.ip, port=self.port + 1)
            except OSError:
               self.initial_server.shutdown_gracefully()
               raise PortInUseError(self.port)

            self.server.set_fn_new_client(self.main_server_new_client)

            print(f"Hosting server at IP address {socket.gethostbyname(socket.gethostname())} on port {self.port}. "
                  "Share this with friends to play together!")

            self.server.run_forever()

        elif self.protocol == "UDP":

            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                self.server.bind((self.ip, self.port + 1))
            except OSError:
                self.initial_server.shutdown_gracefully()
                raise PortInUseError(self.port)

            print(f"Hosting server at IP address {socket.gethostbyname(socket.gethostname())} on port {self.port}. "
                  "Share this with friends to play together!")

    def send(self, msg, client):
        if self.protocol == "TCP":
            self.server.send(msg, client)

        elif self.protocol == "UDP":
            self.server.sendto(str.encode(msg), client)

    def send_to_all(self, msg):
        if self.protocol == "TCP":
            self.server.send_message_to_all(msg)

        elif self.protocol == "UDP":
            self.server.sendto(str.encode(msg), (self.ip, self.port + 1))

    # -------------------------------------------------------------------------------- #

    def set_msg_received_func(self, func):
        if self.protocol == "TCP":
            self.server.set_fn_message_received(func)

        else:
            self.server.on_message = func


# ---------------------------------------------------------------------------------------- #


class MultiplayerClient:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None
        self.protocol = None
        self.connect()

    def connect(self):
        try:
            ws = websocket.WebSocket()
            ws.connect(f"ws://{self.ip}:{self.port}")
            main_server = ws.recv()
            ws.close()
        except OSError:
            raise ServerRefusedError(self.ip, self.port)

        if match("ws://", main_server):

            self.protocol = "TCP"

            # Connect to TCP server
            self.server = websocket.WebSocketApp(main_server, on_message=self.on_message)



        else:

            # Connect to UDP server
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send(self, msg):
        if self.protocol == "TCP":
            self.server.send(msg)

        else:
            self.server.sendto(str.encode(msg), (self.ip, self.port + 1))

    def on_message(self, message):
        pass

    def set_msg_received_func(self, func):
        if self.protocol == "TCP":
            self.server.on_message = func
