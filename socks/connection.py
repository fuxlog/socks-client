import socket
from constants import BUFFER_SIZE, AuthenticationStatus, Method, General
from reply import ConnectionReply, AuthenticationReply, CryptoReply
from request import ConnectionRequest, AuthenticationRequest, CryptoRequest
from session import Session


def proxy_connection(session, proxy):
    connection_request = ConnectionRequest(General.VERSION, (Method.USERNAME_PASSWORD,))
    request = CryptoRequest(session)
    msg_send = request.to_bytes(connection_request.to_bytes())
    proxy.sendall(msg_send)

    msg_recv = proxy.recv(BUFFER_SIZE)
    reply = CryptoReply(session)
    if reply.from_bytes(msg_recv) is False:
        return False

    connection_reply = ConnectionReply()
    if connection_reply.from_bytes(reply.data):
        if connection_reply.method == Method.USERNAME_PASSWORD:
            return True

    return False


def username_password_authenticate(session: Session, proxy: socket.socket, username: str, password: str):
    authentication_request = AuthenticationRequest(General.AUTHENTICATION_VERSION, username, password)
    request = CryptoRequest(session)
    msg_send = request.to_bytes(authentication_request.to_bytes())
    proxy.sendall(msg_send)

    msg_recv = proxy.recv(BUFFER_SIZE)
    reply = CryptoReply(session)
    if reply.from_bytes(msg_recv) is False:
        return False

    authentication_reply = AuthenticationReply()
    if authentication_reply.from_bytes(reply.data):
        if authentication_reply.status == AuthenticationStatus.SUCCESS:
            session.password = password
            return True

    return False
