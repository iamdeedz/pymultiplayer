from pymultiplayer.client import MultiplayerClient


async def msg_handler(msg, websocket):
    print("server sent:", msg)


async def proxy(websocket):
    print("Connected")
    msg = input("enter message: ")
    await websocket.send(msg)
    await client.msg_handler(websocket)


if __name__ == "__main__":
    client = MultiplayerClient(msg_handler)
    client.run(proxy)
