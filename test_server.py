from pymultiplayer import TCPMultiplayerServer
from json import dumps

clients_to_players = {}


class Player:
    def __init__(self, id):
        self.x = id * 25
        self.y = 0
        self.width = self.height = 25
        self.colour = (10 * id, 10 * id, 10 * id)


def new_client(client, server):
    server.clients.append(client)
    clients_to_players[client['id']] = Player(client['id'])
    server.send_message(client, dumps({"type": "greeting", "data": Player(client['id']).__dict__}))
    print("Sending sync message")
    server.send_message(client, dumps({"type": "sync", "data": str(clients_to_players)}))
    print(f"Client with id {client['id']} joined the server.")


def msg_received(client, server, message):
    print(f"Client with id {client['id']} sent message: {message}")
    for c in server.clients:
        if c['id'] != client['id']:
            clients_to_players[client['id']].x = message["data"][0]
            clients_to_players[client['id']].y = message["data"][1]
            server.send_message(c, {"type": "sync", "data": str(clients_to_players)})


def client_left(client, server):
    print(f"Client with id {client['id']} left the server.")


# Create a server object
server = TCPMultiplayerServer()

server.set_new_client_func(new_client)
server.set_msg_received_func(msg_received)
server.set_client_left_func(client_left)

server.run_forever()
