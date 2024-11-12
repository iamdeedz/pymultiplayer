// Notice:
// My Javascript skills were limited when I actually used the language, however I haven't wrote proper code in a good while so I can barely even write any code.
// I am just porting the TCPMultiplayerServer class from the Python code into Javascript.
// If there is something here that I am doing absolutely horribly, please feel free to create a pull request.

import InitialServer from "./InitialServer.js"

module.exports = 0;


class TCPMultiplayerServer {
    constructor(ip="127.0.0.1", port=1300, auth_func=None) {
        this.ip = ip
        this.port = port
        this.clients = [];
        this.last_id = 0
        this.initial_server = new InitialServer(this.ip, this.port, auth_func)
        this.ws = new WebSocket.Server({
            ip: this.ip,
            port: this.port
        })
        this.ws.on("connection", this.client_joined_func)

        this.user_client_joined_func = None
        this.user_client_left_func = None
    }

    broadcast(msg) {
        this.clients.forEach(client => {
            client.ws.send(msg)
        });
    }

    send_to_all_except(client_not_receiving, msg) {
        this.clients.forEach(client => {
            if (client != client_not_receiving) {
                client.ws.send(msg)
            }
        });
    }

    send(client, msg) {
        client.ws.send(msg)
    }

    client_joined_func() {
        new_client = new _Client(websocket)
        this.last_id += 1
    }

    set_client_joined_func(func) {
        this.user_client_joined_func = func
    }

    set_client_left_func(func) {
        this.user_client_left_func = func
    }

    set_msg_received_func(func) {
        this.ws.on("message", func)
    }

    run() {

    }
}