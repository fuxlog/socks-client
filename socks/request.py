class ConnectionRequest():
    def __init__(self, version: int, methods: set) -> None:
        self.version = version
        self.methods = methods

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + len(self.methods).to_bytes(1, "big") + bytes(self.methods)


class AuthenticationRequest():
    def __init__(self, version: int, uname: str, pword: str):
        self.version = version
        self.uname = uname
        self.pword = pword

    def to_bytes(self):
        return self.version.to_bytes(1, "big") + len(self.uname).to_bytes(1, "big") + self.uname.encode() \
                + len(self.pword).to_bytes(1, "big") + self.pword.encode()