from pymultiplayer import TCPMultiplayerServer


def msg_received(client, msg):
    print(f"Client with id: {client['id']} sent message: {msg}")

    server.send_to_all(f"Client with id: {client['id']} sent message: {msg}")


# Create a server object
server = TCPMultiplayerServer()

server.set_msg_received_func(msg_received)
