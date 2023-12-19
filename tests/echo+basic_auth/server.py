from pymultiplayer.TCPserver import TCPMultiplayerServer
from json import dumps
import websockets


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg["content"])
    print("Sending back:", msg["content"])
    await client.ws.send(dumps(msg))


async def auth_func(websocket):
    # This is a very basic authentication function. It connects to an external server and sends the name and password
    # sent by the client. If the server responds with "success", the client is authenticated. Otherwise, the client
    # is not authenticated and the connection is closed.

    # You do not need to use an external server to authenticate clients. You can use a database for example. This is
    # just an example.

    print("Authenticating...")
    await websocket.send("login")
    name = await websocket.recv()
    password = await websocket.recv()
    async with websockets.connect("ws://localhost:3000") as ws:
        await ws.recv()
        await ws.send(name)
        await ws.send(password)
        response = await ws.recv()
        await ws.close()

    if response == "success":
        print("Authenticated.")
        msg = {"type": "authentication", "content": "success"}
        await websocket.send(dumps(msg))

    else:
        print("Authentication failed.")
        msg = {"type": "authentication", "content": "failure"}
        await websocket.send(dumps(msg))
        await websocket.close()


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler, auth_func=auth_func)
    server.run()
