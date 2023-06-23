from websocket_server import WebsocketServer
from re import match
from .errors import *
from multiprocessing import Process
import websocket
import socket
import rel


class UDPMultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None
        self.msg_handler = None
        self.clients = []
        self.initial_server = InitialServer(ip, port)
        self.start()

    def start(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self.server.bind((self.ip, self.port + 1))

        except OSError:
            self.initial_server.server.shutdown_gracefully()
            raise PortInUseError(self.port)

        Process(target=self.msg_handler).start()

        print(f"Hosting server at IP address {socket.gethostbyname(socket.gethostname())} on port {self.port}. "
              "Share this with friends to play together!")

    def close(self):

        self.server.close()

    def send(self, msg, client):
        self.server.sendto(str.encode(msg), client)

    def send_to_all(self, msg):
        for client in self.clients:
            self.server.sendto(str.encode(msg), client)

    def msg_received(self, msg, client):
        pass

    def new_client(self, client, server):
        pass

    def client_left(self, client, server):
        pass

    def set_msg_received_func(self, func):
        self.msg_received = func  # NOQA

    def set_new_client_func(self, func):
        self.new_client = func  # NOQA

    def set_client_left_func(self, func):
        self.client_left = func  # NOQA

    def msg_handler(self):
        while True:
            msg, client = self.server.recvfrom(1024)

            if match("greeting", msg.decode()):
                self.clients.append(client)
                self.new_client(client, self.server)
                continue

            if match("goodbye", msg.decode()):
                self.clients.remove(client)
                self.client_left(client, self.server)
                continue

            self.msg_received(msg, client)


class TCPMultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None
        self.clients = []
        self.initial_server = InitialServer(ip, port)
        self.start()

    def start(self):
        try:
            self.server = WebsocketServer(host=self.ip, port=self.port + 1)
        except OSError:
            self.initial_server.server.shutdown_gracefully()
            raise PortInUseError(self.port)

        self.server.set_fn_new_client(self.new_client)

        print(f"Hosting server at IP address {socket.gethostbyname(socket.gethostname())} on port {self.port}. "
              "Share this with friends to play together!")

    def run_forever(self):
        self.server.run_forever()

    def send(self, msg, client):
        self.server.send(msg, client)

    def send_to_all(self, msg):
        self.server.send_to_all(msg)

    def new_client(self, client, server):
        self.clients.append(client)

    def msg_received(self):
        pass

    def set_msg_received_func(self, func):
        self.server.set_fn_message_received(func)

    def set_new_client_func(self, func):
        self.server.set_fn_new_client(func)

    def set_client_left_func(self, func):
        self.server.set_fn_client_left(func)


# ---------------------------------------------------------------------------------------- #


class InitialServer:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None
        self.start()

    def start(self):
        try:
            self.server = WebsocketServer(host=self.ip, port=self.port)
        except OSError:
            raise PortInUseError(self.port)
        self.server.set_fn_new_client(self.new_client)
        self.server.run_forever(threaded=True)

    def send_to_main_server(self):
        self.server.send_message_to_all(f"ws://{self.ip}:{self.port + 1}")

    def new_client(self, client, server):
        self.send_to_main_server()

    def set_new_client_func(self, func):
        self.server.set_fn_new_client(func)


# ---------------------------------------------------------------------------------------- #


class MultiplayerClient:
    def __init__(self, ip="127.0.0.1", port=1300, tick_func=None, args=()):

        if tick_func is None:
            raise NoTickFunctionError()

        else:
            self.tick_func = tick_func
            self.tick_func_args = (self,) + args

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
            self.server = websocket.WebSocketApp(main_server)

            self.server.run_forever(dispatcher=rel)

            rel.signal(2, self.disconnect)
            rel.timeout(1, self.tick_func, *self.tick_func_args)

            try:
                rel.dispatch()

            except ConnectionResetError:
                raise ServerClosedError()

        else:

            # Connect to UDP server
            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            Process(target=self.msg_handler).start()
            self.server.sendto(str.encode("greeting"), (self.ip, self.port + 1))

    def disconnect(self):
        if self.protocol == "TCP":
            self.server.send("goodbye")

        else:
            self.server.sendto(str.encode("goodbye"), (self.ip, self.port + 1))

        rel.abort()

    def send(self, msg):
        if self.protocol == "TCP":
            self.server.send(msg)
        else:
            self.server.sendto(str.encode(msg), (self.ip, self.port + 1))

    def msg_received(self, msg):
        pass

    def on_error(self, ws, error):
        pass

    def on_close(self):
        pass

    def set_msg_received_func(self, func):
        if self.protocol == "TCP":
            self.server.on_message = func

        else:
            self.msg_received = func  # NOQA

    def set_on_error_func(self, func):
        if self.protocol == "TCP":
            self.server.on_error = func

        else:
            print("The host is using a UDP based server which does not support error handling.")

    def set_on_close_func(self, func):
        if self.protocol == "TCP":
            self.server.on_close = func

        else:
            self.on_close = func  # NOQA

    def msg_handler(self):
        while True:
            msg, _ = self.server.recvfrom(1024)

            if match("close", msg.decode()):
                self.on_close()

            self.msg_received(msg.decode())
