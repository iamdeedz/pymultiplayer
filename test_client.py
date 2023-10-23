from pymultiplayer.client import MultiplayerClient


async def auth_handler(websocket):
    await websocket.recv()
    name = input("Enter name: ")
    password = input("Enter password: ")
    await websocket.send(name)
    await websocket.send(password)
    response = await websocket.recv()
    if response == "success":
        print("Authenticated.")
        
    else:
        print("Authentication failed.")
        await websocket.close()


async def msg_handler(msg, websocket):
    print("server sent:", msg)


async def proxy(websocket):
    print("Connected")
    msg = input("enter message: ")
    await websocket.send(msg)
    await client.msg_handler(websocket)


if __name__ == "__main__":
    client = MultiplayerClient(msg_handler, auth_handler=auth_handler)
    client.run(proxy)
