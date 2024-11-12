// Notice:
// My Javascript skills were limited when I actually used the language, however I haven't wrote proper code in a good while so I can barely even write any code.
// I am just porting the InitialServer class from the Python code into Javascript.
// If there is something here that I am doing absolutely horribly, please feel free to create a pull request.

const WebSocket = require("ws");


class InitialServer {
    constructor(ip="127.0.0.1", port=1300, auth_func=None) {
        this.ip = ip;
        this.port = port;
        this._auth_func = auth_func;
    }

    start() {
        const wss = new WebSocket.Server({
            ip: this.ip,
            port: this.port
        });
    }

    new_client(websocket) {
        if (this._auth_func) {
            this._auth_func(websocket)
        }

        const msg = {"type": "uri", "content": "ws://" + this.ip + ":" + (this.port + 1)}
        websocket.send(JSON.stringify(msg))
        websocket.close()
    }
}