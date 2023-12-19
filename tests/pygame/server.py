from pymultiplayer import TCPMultiplayerServer
from json import dumps


async def msg_handler(msg, client):
    if msg["type"] == "update":
        server.send_to_all_except(client, dumps(msg))


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.run()
