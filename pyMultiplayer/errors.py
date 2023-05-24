class PortInUseError(Exception):
    def __init__(self, port):
        self.message = f"Port {port} is already in use."
        super().__init__(self.message)


class InvalidProtocolError(Exception):
    def __init__(self, protocol):
        self.message = f'Invalid protocol "{protocol}"'
        super().__init__(self.message)


class ServerRefusedError(Exception):
    def __init__(self, ip, port):
        self.message = f"The server at {ip}:{port} refused the connection. This is likely due to the server not " \
                        f"existing (not at that port at least)."
        super().__init__(self.message)


class NoTickFunctionError(Exception):
    def __init__(self):
        self.message = "No tick function was provided."
        super().__init__(self.message)
