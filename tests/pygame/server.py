from pymultiplayer import TCPMultiplayerServer
from json import dumps


def client_joined(client):
    print(f"Client with id {client.id} connected")
    msg_to_send = {"type": "client_joined", "content": client.id}
    server.broadcast(dumps(msg_to_send))


def client_left(client):
    print(f"Client with id {client.id} disconnected")
    msg_to_send = {"type": "client_left", "content": client.id}
    server.broadcast(dumps(msg_to_send))


async def msg_handler(msg, client):
    if msg["type"] == "update":
        print(f"Client with id {client.id} sent an update")
        print(msg["content"])
        server.send_to_all_except(client, dumps(msg))


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()
