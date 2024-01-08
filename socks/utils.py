from .constants import PUBLIC_KEY
import socket


class Storage:
    def __init__(self) -> None:
        self.username = None
        self.password = None


class Session:
    def __init__(self) -> None:
        self.browser_addr = None
        self.sock = None
        self.key = PUBLIC_KEY
