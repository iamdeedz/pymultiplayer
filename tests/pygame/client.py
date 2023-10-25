from pymultiplayer import MultiplayerClient
from json import dumps, loads
import pygame as p

id = None


async def main():
    pass


async def msg_handler(msg_json, client):
    pass

async def proxy(websocket):
    await client.msg_handler()


if __name__ == "__main__":
    p.init()
    p.display.set_caption("Multiplayer Test")
    screen = p.display.set_mode((500, 500))
    clock = p.time.Clock()

    client = MultiplayerClient(msg_handler)
    client.run(proxy)
