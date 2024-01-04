class ConnectionRequest():
    def __init__(self, version: int, nmethods: int, methods: set) -> None:
        self.version = version
        self.nmethod = nmethods
        self.methods = methods

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + self.nmethod.to_bytes(1, "big") + bytes(self.methods)


class AuthenticationRequest():
    def __init__(self, version: int, uname: str, pword: str):
        self.version = version
        self.uname = uname
        self.pword = pword

    def to_bytes(self):
        return self.version.to_bytes(1, "big") + len(self.uname).to_bytes(1, "big") + self.uname.encode() \
                + len(self.pword).to_bytes(1, "big") + self.pword.encode()