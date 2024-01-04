import socket
import threading
from config import CLIENT_HOST, CLIENT_PORT, PROXY_HOST, PROXY_PORT
from socks.authenticate import proxy_connection_authenticate
from socks.constants import BUFFER_SIZE

class Session:
    def __init__(self, addr, username, password) -> None:
        self.addr = addr
        self.username = username
        self.password = password


def welcome():
    print("Welcome to FUXLOGSOCKS client")
    print("    1. Connect to proxy")
    print("    2. Register")
    print("    0. Exit")


def authenticate():
    print("Authentication USERNAME/PASSWORD")
    username = input("Username: ")
    password = input("Password: ")
    return username, password


def register():
    print("Register USERNAME/PASSWORD")
    username = input("Username: ")
    password = input("Password: ")
    return username, password


def user_select() -> int:
    user = input("[USER] > ")
    if user != "1" and user != "2" and user != "0":
        print("Invalid input from user")
        return -1
    return int(user)


def start():
    welcome()
    while True:
        user = user_select()
        if user == 0:
            break
        if user == 1:
            username, password = authenticate()
            session = Session(None, username, password)
            session_listen(session, CLIENT_HOST, CLIENT_PORT)
        if user == 2:
            print(register())


def handle(browser: socket.socket, session: Session):
    try:
        proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy.connect((PROXY_HOST, PROXY_PORT))
        print(f"[INFO] Found proxy server {(PROXY_HOST, PROXY_PORT)}")
    except socket.error as e:
        print(e)
        return
    
    if proxy_connection_authenticate(proxy, session.username, session.password) is False:
        print(f"[INFO] {session.addr} Authenticate with proxy server failed")
        return


    print(f"[INFO] {session.addr} connected to FUXLOGSOCKS client")
    # Browser send VERSION 5, NO AUTHENTICATION REQUIRED
    data = browser.recv(4096)
    if not data:
        return
    # Client send reply to accept browser
    browser.sendall(b"\x05\x00")

    while True:
        browser_data = browser.recv(BUFFER_SIZE)
        proxy.sendall(browser_data)

        proxy_data = proxy.recv(BUFFER_SIZE)
        browser.sendall(proxy_data)

        if not browser_data:
            print(f"[INFO] {session.addr} close connection")
            break

        print(f"[INFO] {session.addr} : {browser_data}")


def session_listen(session: Session, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((host, port))
    client.listen(20)
    print(f"[INFO] Client start listening on {(host, port)}")
    while True:
        browser, addr = client.accept()
        session.addr = addr
        browser_handler = threading.Thread(target=handle, args=(browser, session, ))
        browser_handler.start()

    
if __name__ == "__main__":
    start()