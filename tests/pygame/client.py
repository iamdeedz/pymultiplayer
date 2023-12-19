from pymultiplayer import MultiplayerClient
from json import dumps, loads
from player import Player
import pygame as p

self = None
other_players = []


def send_update():
    msg = {"type": "update", "content": {"x": self.x, "y": self.y}, "id": id}
    client.ws.send(dumps(msg))


async def main():
    for event in p.event.get():
        if event.type == p.QUIT:
            global running
            running = False

    screen.fill((0, 0, 0))
    for player in other_players:
        p.draw.rect(screen, player.colour, (player.x, player.y, player.width, player.height))
    p.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
    p.display.update()


async def msg_handler(msg):
    if msg["type"] == "client_joined":
        global other_players
        other_players.append(Player(msg["content"]))


async def proxy(websocket):
    global self
    self = Player(client.id)
    while running:
        await client.msg_handler()
        await main()


if __name__ == "__main__":
    p.init()
    p.display.set_caption("Multiplayer Test")
    screen = p.display.set_mode((500, 500))
    clock = p.time.Clock()
    running = True

    client = MultiplayerClient(msg_handler)
    client.run(proxy)
