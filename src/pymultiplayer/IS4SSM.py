import websockets, asyncio
from .errors import PortInUseError, AuthServerOffline
from json import dumps, loads
from .health_check import health_check


class InitialServerForSSM:
    """
    A version of the 'initial_server' class that is used for 'TCPMultiplayerServer's in use by the 'StaticServerManager' class.
    """
    def __init__(self, sm_uuid, ip="127.0.0.1", port=1300, auth_func=None, ws_or_wss: str = "ws"):
        self.ip = ip
        self.port = port
        self.ws_or_wss = ws_or_wss
        self.sm_uuid = sm_uuid
        self._auth_func = auth_func

    async def _start(self):
        try:
            async with websockets.serve(self.new_client, self.ip, self.port, process_request = health_check):
                await asyncio.Future()
        except OSError:
            raise PortInUseError(self.port)

    async def new_client(self, websocket):
        incoming_msg = loads(await websocket.recv())
        if "uuid" in incoming_msg:
            # Request is supposedly from server
            if incoming_msg["uuid"] != self.sm_uuid:
                # Request is not legitimate
                msg = {"type": "error", "content": "UUID is invalid."}
                await websocket.send(dumps(msg))
                await websocket.close()
                return

            # Request is legitimately from server
            print(incoming_msg)

            await websocket.close()

        else:
            # Request is from a client
            if self._auth_func:
                try:
                    await self._auth_func(websocket)
                except OSError:
                    msg = {"type": "error", "content": "Server encountered an OSError during the authentication process."}
                    await websocket.send(dumps(msg))
                    await websocket.close()
                    raise AuthServerOffline()

            msg = {"type": "uri", "content": f"{self.ws_or_wss}://{self.ip}:{self.port + 1}"}
            await websocket.send(dumps(msg))
            await websocket.close()

    def start(self):
        asyncio.run(self._start())
