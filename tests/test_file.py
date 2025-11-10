import websockets
from json import loads, dumps
from asyncio import run
from time import sleep
from pymultiplayer import MultiplayerClient, StaticServerManager, ServerOptions


async def test1():
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({}))
        print(loads(await websocket.recv()))


async def test2():
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"uuid": "abcd"}))
        print(loads(await websocket.recv()))


async def test3():
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"uuid": "36298555-7e8f-4965-aaf3-265564ee637e", "type": "testing", "content": "this is the content field"}))
        print(loads(await websocket.recv()))


async def test4():
    """
    Create server - no parameters
    """
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "create"}))


async def test5():
    """
    Create server - with parameters
    """
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "create", "parameters": {"level_id": -999, "max_players": 2}}))
        print(loads(await websocket.recv()))


async def test6():
    """
    Get servers
    """
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "get"}))
        print(loads(await websocket.recv()))


async def test7():
    """
    Connect to server number one, enter receive mode
    """
    async with websockets.connect("ws://127.0.0.1:1302") as websocket:
        await websocket.send(dumps({"type": ""}))
        async for msg_json in websocket:
            print(loads(msg_json))


async def test8():
    """
    Connect to server number one with multiplayer client and finish game after 2 seconds
    """
    async def msg_handler(msg):
        print("Server sent: " + str(msg))

    client = MultiplayerClient(msg_handler, port=1301)
    client.start()
    print("after start")
    sleep(2)
    print("closing")
    await client.send(dumps({"type": "game_complete", "content": ""}))


async def test9():
    """
    Connect to server number one with multiplayer client
    """
    async def msg_handler(msg):
        print("Server sent: " + str(msg))
    client = MultiplayerClient(msg_handler, port=1301)
    client.start()


def msg_handler(client, msg):
    print(f"client {client.id} sent: {msg}")


def test10():
    """
    Create an SSM
    """
    ssm = None


    server_options = ServerOptions(msg_handler)
    ssm = StaticServerManager(3)
    ssm.run(server_options)

if __name__ == "__main__":
    test_num = input("Which test? ")

    while test_num not in ["1","2","3","4","5","6","7","8","9","10"]:
        print("Test number must be 1, 2, 3, 4, 5, 6, 7, 8, 9, or 10")
        test_num = input("Which test? ")

    exec(f"run(test{test_num}())")
