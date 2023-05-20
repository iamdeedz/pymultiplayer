from websocket_server import WebsocketServer
import websocket
from re import match


class MultiplayerServer:
    def __init__(self, ip="127.0.0.1", port=1300, protocol="TCP"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.sockets = []
        self.initial_server = None
        self.server = None
        self.start()

    def start(self):
        self.start_initial_server()
        self.start_main_server()

    def start_initial_server(self):
        self.initial_server = WebsocketServer(host=self.ip, port=self.port)
        self.initial_server.set_fn_new_client(self.new_client)
        self.initial_server.run_forever()

    def new_client(self, client, server):
        self.send_to_main_server()

    def send_to_main_server(self):
        if self.protocol == "TCP":
            self.initial_server.send_message_to_all(f"ws://{self.ip}:{self.port+1}")
        elif self.protocol == "UDP":
            pass
        else:
            self.initial_server.shutdown_gracefully()
            raise Exception("Invalid protocol")

    def start_main_server(self):
        if self.protocol == "TCP":

            self.server = WebsocketServer(host=self.ip, port=self.port+1)
            self.server.set_fn_new_client(self.new_client)
            self.server.set_fn_message_received(self.message_received)
            self.server.run_forever()

        else:
            self.initial_server.shutdown_gracefully()
            raise Exception("Invalid protocol")

    # -------------------------------------------------------------------------------- #

    def set_msg_received_func(self, func):
        self.server.set_fn_message_received(func)

    def set_new_client_func(self, func):
        self.server.set_fn_new_client(func)

    def set_client_left_func(self, func):
        self.server.set_fn_client_left(func)


# ---------------------------------------------------------------------------------------- #


class MultiplayerClient:
    def __init__(self, ip="127.0.0.1", port=1300):
        self.ip = ip
        self.port = port
        self.server = None

    def connect(self):
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.ip}:{self.port}")
        main_server = ws.recv()
        ws.close()
        if match("ws://", main_server):
            # Connect to TCP server
            self.server = websocket.WebSocketApp(main_server, on_message=self.on_message)
            self.server.run_forever()
        else:
            # Connect to UDP server
            pass

    def on_message(self, ws, message):
        pass
