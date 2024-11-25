class PortInUseError(Exception):
    def __init__(self, port):
        self.message = f"Port {port} is already in use."
        super().__init__(self.message)


class ServerUnreachableError(Exception):
    def __init__(self, ip, port):
        self.message = f"The server at {ip}:{port} could not be reached."
        super().__init__(self.message)


class AuthServerOffline(Exception):
    def __init__(self):
        self.message = "The provided authentication server could not be reached."
        super().__init__(self.message)


class ServerClosedError(Exception):
    def __init__(self):
        self.message = "The server forcibly closed the connection. This is likely due to the server encountering an error." # NOQA
        super().__init__(self.message)


class ServerError(Exception):
    def __init__(self, msg):
        self.message = f"The server encountered an error and had to close the connection. It sent this error: {msg}"
        super().__init__(self.message)


class NoParametersGiven(Exception):
    def __init__(self):
        self.message = "No parameters were given in the create server request."
        super().__init__(self.message)
