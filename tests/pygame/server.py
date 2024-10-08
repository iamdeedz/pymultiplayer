from pymultiplayer import TCPMultiplayerServer
from player import Player
from json import dumps

players = list()
id_to_player = dict()


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg["content"])
    players[client.id-1][1] = msg["content"]["x"]
    players[client.id-1][2] = msg["content"]["y"]
    await server.broadcast(dumps(msg))


async def client_joined(client):
    print(f"Client with id {client.id} joined.")

    # Tell all existing clients the new client's id
    msg = {"type": "client_joined", "content": client.id}
    await server.send_to_all_except(client, dumps(msg))

    # Bring the new client up to speed with all the other clients
    msg = {"type": "sync", "content": players}
    print(f"Players: {players}")
    await server.send(client, dumps(msg))
    # Keep track of all players
    player = Player(client.id)
    players.append([player.id, player.x, player.y])
    id_to_player[client.id] = player


async def client_left(client):
    print(f"Client with id {client.id} left.")
    msg = {"type": "client_left", "content": client.id}
    await server.broadcast(dumps(msg))
    players.remove(id_to_player[client.id])
    id_to_player[client.id] = None


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.set_client_joined_func(client_joined)
    server.set_client_left_func(client_left)
    server.run()
