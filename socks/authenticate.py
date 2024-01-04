import socket
from .constants import BUFFER_SIZE, AuthenticationStatus, Method, General
from .reply import ConnectionReply, AuthenticationReply
from .request import ConnectionRequest, AuthenticationRequest


def proxy_connection_authenticate(proxy: socket.socket, username: str, password: str):
    connection_request = ConnectionRequest(General.VERSION, 1, (Method.USERNAME_PASSWORD))
    proxy.sendall(connection_request.to_bytes())

    data = proxy.recv(BUFFER_SIZE)
    reply = ConnectionReply()

    if reply.from_bytes(data) is True:
        if reply.method == Method.USERNAME_PASSWORD:
            authentication_request = AuthenticationRequest(General.AUTHENTICATION_VERSION, username, password)
            proxy.sendall(authentication_request.to_bytes())

            data = proxy.recv(BUFFER_SIZE)
            authentication_reply = AuthenticationReply()

            if authentication_reply.from_bytes(data) is True:
                if authentication_reply.status == AuthenticationStatus.SUCCESS:
                    return True
    
    return False