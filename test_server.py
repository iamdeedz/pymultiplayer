from pymultiplayer.TCPserver import TCPMultiplayerServer

async def proxy(websocket):
    print("Connected")
    msg = await websocket.recv()
    print(f'client sent "{msg}"')
    print("Sending message back to client...")
    await websocket.send(msg)


if __name__ == "__main__":
    server = TCPMultiplayerServer()
    server.run(proxy)
