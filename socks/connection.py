import socket
from .constants import AuthenticationStatus, Method, General
from .reply import ConnectionReply, AuthenticationReply
from .request import ConnectionRequest, AuthenticationRequest, ChangePasswordRequest
from .utils import Session
from .cryption import send_encrypted, recv_decrypted


def connection(session: Session):
    # Connection request and encrypt message with session.key
    connection_request = ConnectionRequest(General.VERSION, (Method.USERNAME_PASSWORD,))

    send_encrypted(session, connection_request.to_bytes())
    data = recv_decrypted(session)

    # Handle connection reply
    connection_reply = ConnectionReply()
    if connection_reply.from_bytes(data):
        # Only using USERNAME/PASSWORD authentication
        if connection_reply.method == Method.USERNAME_PASSWORD:
            return True

    return False


def username_password_authenticate(session: Session, version: int, username: str, password: str):
    # Authentication request and encrypt message with session.key
    authentication_request = AuthenticationRequest(version, username, password)

    send_encrypted(session, authentication_request.to_bytes())
    data = recv_decrypted(session)

    # Handle authentication reply
    authentication_reply = AuthenticationReply()
    if authentication_reply.from_bytes(data):
        if authentication_reply.status == AuthenticationStatus.SUCCESS:
            return True

    return False


def username_password_register(session: Session, username: str, password: str):
    # Authentication request and encrypt message with session.key
    authentication_request = AuthenticationRequest(General.REGISTER_VERSION, username, password)
 
    send_encrypted(session, authentication_request.to_bytes())
    data = recv_decrypted(session)
 
    # Handle authentication reply
    authentication_reply = AuthenticationReply()
    if authentication_reply.from_bytes(data):
        if authentication_reply.status == AuthenticationStatus.SUCCESS:
            print("[INFO] Register successfully")
            return True
 
    print("[INFO] Register failed")
    return False


def change_password_request(session: Session, username: str, new_pword: str):
    change_password_request = ChangePasswordRequest(General.MODIFIED_VERSION, username, new_pword)

    send_encrypted(session, change_password_request.to_bytes())
    data = recv_decrypted(session)

    # Handle authentication reply
    authentication_reply = AuthenticationReply()
    if authentication_reply.from_bytes(data):
        if authentication_reply.status == AuthenticationStatus.SUCCESS:
            print("[INFO] Change password successfully")
            return True
        
    print("[INFO] Change password failed")
    return False
