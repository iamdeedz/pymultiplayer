from pymultiplayer.TCPserver import TCPMultiplayerServer


async def msg_handler(msg, websocket):
    print("client sent:", msg)
    print("sending back:", msg)
    await websocket.send(msg)


async def proxy(websocket):
    print("Connected")
    await server.msg_handler(websocket)


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.run(proxy)
