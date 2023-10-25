from pymultiplayer import TCPMultiplayerServer
from json import dumps, loads


async def msg_handler(msg, client):
    if msg["type"] == "greeting":
        await client.ws.send(dumps())


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.run()
