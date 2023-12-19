from pymultiplayer import TCPMultiplayerServer
from json import dumps, loads


async def msg_handler(msg, client):
    if msg["type"] == "greeting":
        msg_to_send = {"type": "greeting", "content": server.clients[-1].id}
        await client.ws.send(msg_to_send)

        msg_to_send = {"type": "client_joined", "content": client.id}
        server.send_to_all_except(client, dumps(msg_to_send))

    elif msg["type"] == "update":
        server.send_to_all_except(client, dumps(msg))


if __name__ == "__main__":
    server = TCPMultiplayerServer(msg_handler)
    server.run()
