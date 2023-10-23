from pymultiplayer.TCPserver import TCPMultiplayerServer
import websockets


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg)
    print("Sending back:", msg)
    await client.ws.send(msg)


async def auth_func(websocket):
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
        await websocket.send("success")

    else:
        print("Authentication failed.")
        await websocket.send("failure")
        await websocket.close()



if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler, auth_func=auth_func)
    server.run()
