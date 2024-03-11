from pymultiplayer import TCPMultiplayerServer
from json import dumps


def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg["content"])
    print("Broadcasting")
    server.broadcast(dumps(msg))


def client_joined(client):
    print(f"Client with id {client.id} joined.")
    msg = {"type": "client_joined", "content": client.id}
    server.send_to_all_except(client, dumps(msg))


def client_left(client):
    print(f"Client with id {client.id} left.")
    msg = {"type": "client_left", "content": client.id}
    server.broadcast(dumps(msg))


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()
