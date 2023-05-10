import websockets
import asyncio
from time import sleep

# ------------------------- #
# Functions to connect #

socket = None


async def connector(port):
    ip = f"ws://localhost:{port}"
    async with websockets.connect(ip) as websocket:
        global socket
        socket = websocket.recv()


def get_socket():
    return socket


def connect(port):
    asyncio.run(connector(port))


# ------------------------- #
# Functions once connected #


def update(socket):
    asyncio.run(updater(socket))


async def updater(socket):
    exec(await socket.recv())


def send(socket, data):
    asyncio.run(sender(socket, data))


async def sender(socket, data):
    await socket.send(data)

# ------------------------- #
