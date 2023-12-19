from pymultiplayer import MultiplayerClient
from json import dumps, loads
from player import Player
import pygame as p

id = None
self = None
other_players = []
velocity = 5


async def main():
    for event in p.event.get():
        if event.type == p.QUIT:
            global running
            running = False

        elif event.type == p.KEYDOWN:
            if event.key == p.K_UP:
                self.y -= velocity

            elif event.key == p.K_DOWN:
                self.y += velocity

            elif event.key == p.K_LEFT:
                self.x -= velocity

            elif event.key == p.K_RIGHT:
                self.x += velocity

    screen.fill((0, 0, 0))
    for player in other_players:
        p.draw.rect(screen, player.colour, (player.x, player.y, player.width, player.height))
    p.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


async def msg_handler(msg_json, client):
    global other_players
    msg = loads(msg_json)
    if msg["type"] == "greeting":
        global id
        id = msg["content"]

    elif msg["type"] == "client_joined":
        other_players.append(Player(msg["content"]))

    elif msg["type"] == "client_left":
        for player in other_players:
            if player.id == msg["content"]:
                other_players.remove(player)
                break


async def proxy(websocket):
    global id
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
