import websockets
import asyncio
from multiprocessing import Process
from time import sleep

sockets = []
global_port = 0


async def connection_handler(websocket):
    print("Connected")
    global sockets
    sockets.append(websocket)
    websocket.send(websocket)
    helper_process = Process(target=start_helper, args=(websocket,))
    helper_process.start()


async def main(port):
    async with websockets.serve(connection_handler, "localhost", port):
        print("Ready to connect.")
        await asyncio.Future()


def host(port):
    global global_port
    global_port = port
    asyncio.run(main(port))


def start_helper(socket):
    asyncio.run(helper(socket))


async def helper(og_socket):
    data = await og_socket.recv()
    for socket in sockets:
        if socket != og_socket:
            await socket.send(data)
