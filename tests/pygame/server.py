from pymultiplayer import TCPMultiplayerServer
from player import Player
from json import dumps

players = list()
id_to_player = dict()


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg["content"])
    server.broadcast(dumps(msg))


async def client_joined(client):
    print(f"Client with id {client.id} joined.")
    msg = {"type": "client_joined", "content": client.id}
    server.send_to_all_except(client, dumps(msg))
    msg = {"type": "sync", "content": players}
    await server.send_to(client, dumps(msg))
    player = Player(client.id)
    players.append([player.id, player.x, player.y])
    id_to_player[client.id] = player


async def client_left(client):
    print(f"Client with id {client.id} left.")
    msg = {"type": "client_left", "content": client.id}
    server.broadcast(dumps(msg))
    print(id_to_player)
    print(id_to_player[client.id])
    players.remove(id_to_player[client.id])


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()
