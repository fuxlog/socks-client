class ConnectionReply:

    def __init__(self):
        self.version = None
        self.method = None

    def from_bytes(self, data: bytes):
        if len(data) != 2:
            return False

        self.version = data[0]
        self.method = data[1]

        return True


class AuthenticationReply:

    def __init__(self):
        self.version = None
        self.status = None

    def from_bytes(self, data: bytes) -> bool:
        if len(data) != 2:
            return False

        self.version = data[0]
        self.status = data[1]

        return True
