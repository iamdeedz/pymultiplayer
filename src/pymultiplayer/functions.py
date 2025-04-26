import websockets
from json import dumps, loads


async def get_servers(ip, port):
    async with websockets.connect(f"ws://{ip}:{port}") as websocket:
        await websocket.send(dumps({"type": "get"}))
        return_msg = loads(await websocket.recv())
        await websocket.close()
        return return_msg


async def create_server(ip, port, parameters: dict):
    async with websockets.connect(f"ws://{ip}:{port}") as websocket:
        await websocket.send(dumps({"type": "create", "parameters": parameters}))
        reply = loads(await websocket.recv())
        await websocket.close()
        return reply


async def get_player_count_of_server(ip, port):
    async with websockets.connect(f"ws://{ip}:{port}") as websocket:
        msg = await websocket.recv()
        uri = loads(msg)["content"]
        if not uri.startswith("ws://"):
            print("Invalid URI")
            await websocket.close()
            quit()

        await websocket.close()

    async with websockets.connect(uri) as websocket:
        await websocket.send(dumps({"type": "get_player_count"}))
        return_msg = loads(await websocket.recv())
        return return_msg
