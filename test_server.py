from pymultiplayer.TCPserver import TCPMultiplayerServer


async def msg_handler(msg, client):
    print(f"Client with id {client.id}:", msg)
    print("Sending back:", msg)
    await client.ws.send(msg)


async def auth_func(websocket):
    print("Authenticating...")
    print("Authenticated!")


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler, auth_func=auth_func)
    server.run()
