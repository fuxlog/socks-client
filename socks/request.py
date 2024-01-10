class ConnectionRequest:
    def __init__(self, version: int, methods: tuple) -> None:
        self.version = version
        self.methods = methods

    def to_bytes(self) -> bytes:
        return self.version.to_bytes(1, "big") + len(self.methods).to_bytes(1, "big") + bytes(self.methods)


class AuthenticationRequest:
    def __init__(self, version: int, uname: str, pword: str):
        self.version = version
        self.uname = uname
        self.pword = pword

    def to_bytes(self):
        return self.version.to_bytes(1, "big") + len(self.uname).to_bytes(1, "big") + self.uname.encode() \
            + len(self.pword).to_bytes(1, "big") + self.pword.encode()


class ChangePasswordRequest:
    def __init__(self, version: int, uname: str, old_pword: str, new_pword: str):
        self.version = version
        self.uname = uname
        self.old_pword = old_pword
        self.new_pword = new_pword

    def to_bytes(self):
        return self.version.to_bytes(1, "big") + len(self.uname).to_bytes(1, "big") + self.uname.encode() \
            + len(self.old_pword).to_bytes(1, "big") + self.old_pword.encode() \
            + len(self.new_pword).to_bytes(1, "big") + self.new_pword.encode()
