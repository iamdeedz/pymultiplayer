from pymultiplayer import MultiplayerClient
from json import dumps, loads
from player import Player
import pygame as p

id = None
self = None
other_players = []


async def main():
    for event in p.event.get():
        if event.type == p.QUIT:
            global running
            running = False


async def msg_handler(msg_json, client):
    if msg["type"] == "client_joined":
        global other_players
        other_players.append(Player(msg["content"]))


async def proxy(websocket):
    global self
    self = Player(id)
    while running:
        await client.msg_handler()
        await main()

    await websocket.close()


if __name__ == "__main__":
    p.init()
    p.display.set_caption("Multiplayer Test")
    screen = p.display.set_mode((500, 500))
    clock = p.time.Clock()
    running = True

    client = MultiplayerClient(msg_handler)
    client.run(proxy)
