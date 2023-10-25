from pymultiplayer.client import MultiplayerClient
from pymultiplayer.errors import ServerError
from json import dumps, loads


async def auth_handler(websocket):
    await websocket.recv()
    name = input("Enter name: ")
    password = input("Enter password: ")
    await websocket.send(name)
    await websocket.send(password)
    response_json = await websocket.recv()
    response = loads(response_json)
    if response["type"] == "error":
        raise ServerError(response["content"])

    elif response["content"] == "success":
        print("Authenticated.")
        
    else:
        print("Authentication failed.")
        await websocket.close()


async def msg_handler(msg_json, websocket):
    msg = loads(msg_json)
    print("server sent:", msg["content"])


async def proxy(websocket):
    print("Connected")
    txt = input("enter message: ")
    msg = {"type": "message", "content": txt}
    await websocket.send(dumps(msg))
    await client.msg_handler(websocket)


if __name__ == "__main__":
    client = MultiplayerClient(msg_handler, auth_handler=auth_handler)
    client.run(proxy)
