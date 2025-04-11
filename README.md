## pymultiplayer
A library for adding multiplayer functionality to python games.

## Note
This is a work in progress. Don't expect all features to work.
I don't know what version of python is needed for this package to work.

This is mainly just a passion project/project to help future projects (in fact I'm using it right now in [Elemental Defense](https://www.github.com/iamdeedz/elemental-defense/)) but it would be nice if it had some use.

---
## Usage

**A full example of this package's usage will be uploaded to [iamdeedz.github.io](https://iamdeedz.github.io) eventually (if I get around to it)!**

---

### Installation
`pip install pymultiplayer` or `python -m pip install pymultiplayer`

---

### Client Representation
The client is represented by a class with the following attributes:
```python
class _Client:
    def __init__(self, ws, id):
        self.ws = ws
        self.id = id
```

#### Parameters
- `ws` - The websocket connection. Used for sending messages with `ws.send()`.
- `id` - The client's id. Used for identifying clients.

The client class is not meant to be initialized by the user. It is created by the server and passed to the message handler function.

---

### MultiplayerClient
```
class MultiplayerClient:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_handler=None):
```

---

### TCPMultiplayerServer
```
class TCPMultiplayerServer:
    def __init__(self, msg_handler, ip="127.0.0.1", port=1300, auth_func=None):
```
#### Parameters
- `msg_handler` - The function that gets ran for every message the server receives. Takes in the message as the first argument and the client as the second. <span style="color:darkred">***REQUIRED***</span>
- `ip` - The ip address the server will run on. Default is localhost or 127.0.0.1.
- `port` - The port the server will run on. Default is 1300.
- `auth_func` - If you want to use authentication, you can pass a function here. If an auth_func is given, it will be run every time a client connects. Takes in the websocket connection. Take a look at [this](tests/echo+basic_auth) example. The auth code is in server.py and authenticator.py.

#### Usage
Full examples of these functions will be uploaded to [iamdeedz.github.io](https://iamdeedz.github.io) in due course but for now, here's a basic example.

Let's start with the server.

First, create a file called `server.py`.

Now, create the required function(s).

```python
# server.py

def msg_handler(msg, client):
    print(f"Received message from {client}: {msg}")
```

Then, create the server object.
```python
# server.py

from pymultiplayer import TCPMultiplayerServer

def msg_handler(msg, client):
    print(f"Received message from {client}: {msg}")

server = TCPMultiplayerServer(msg_handler)

```

Next, run the server.
```python
# server.py

from pymultiplayer import TCPMultiplayerServer

def msg_handler(msg, client):
    print(f"Received message from {client}: {msg}")

server = TCPMultiplayerServer(msg_handler)
server.run()
```
