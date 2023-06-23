from pymultiplayer import TCPMultiplayerServer


def new_client(client, server):
    server.clients.append(client)
    print(f"Client with id {client['id']} joined the server.")


def msg_received(client, server, message):
    print(f"Client with id {client['id']} sent message: {message}")
    for c in server.clients:
        if c['id'] != client['id']:
            server.send_message(c, message)


def client_left(client, server):
    print(f"Client with id {client['id']} left the server.")


# Create a server object
server = TCPMultiplayerServer()

server.set_new_client_func(new_client)
server.set_msg_received_func(msg_received)
server.set_client_left_func(client_left)

server.run_forever()
