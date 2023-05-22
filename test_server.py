import pymultiplayer as pmp


def msg_received(client, msg):
    print(f"Client with id: {client['id']} sent message: {msg}")

    server.send_to_all(f"Client with id: {client['id']} sent message: {msg}")


# Create a server object
server = pmp.MultiplayerServer(protocol="TCP")

server.set_msg_received_func(msg_received)
