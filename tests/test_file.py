import websockets
from json import loads, dumps
from asyncio import run
from time import sleep
from pymultiplayer import MultiplayerClient


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
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "create"}))


async def test5():
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "create", "parameters": {"level_id": -999, "max_players": 2}}))
        print(loads(await websocket.recv()))


async def test6():
    async with websockets.connect("ws://127.0.0.1:1300") as websocket:
        await websocket.send(dumps({"type": "get"}))
        print(loads(await websocket.recv()))


async def test7():
    async with websockets.connect("ws://127.0.0.1:1302") as websocket:
        await websocket.send(dumps({"type": ""}))
        async for msg_json in websocket:
            print(loads(msg_json))


async def test8():
    close = False
    client = None
    async def msg_handler(msg):
        print("Server sent: " + str(msg))
        if close:
            await client.send(dumps({"type": "finish", "content": ""}))
    client = MultiplayerClient(msg_handler, port=1301)
    client.start()
    sleep(2)
    close = True


async def test9():
    async def msg_handler(msg):
        print("Server sent: " + str(msg))
    client = MultiplayerClient(msg_handler, port=1301)
    client.start()


test_num = input("Which test? ")

while test_num not in ["1","2","3","4","5","6","7","8","9"]:
    print("Test number must be 1, 2, 3, 4, 5, 6, 7, 8, or 9")
    test_num = input("Which test? ")

exec(f"run(test{test_num}())")
