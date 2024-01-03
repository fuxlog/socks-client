import socket
import threading
from config import CLIENT_HOST, CLIENT_PORT


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
            print(authenticate())
            listen(CLIENT_HOST, CLIENT_PORT)
        if user == 2:
            print(register())


def handle(browser: socket.socket, addr):
    print(f"[INFO] {addr} connected to FUXLOGSOCKS client")
    data = browser.recv(4096)
    if not data:
        return
    
    browser.sendall(b"\x05\x00")

    while True:
        data = browser.recv(4096)
        if not data:
            print(f"[INFO] {addr} close connection")
            break
        print(f"[INFO] {addr} : {data}")


def listen(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((host, port))
    client.listen(20)
    print(f"[INFO] Client start listening on {(host, port)}")
    while True:
        browser, addr = client.accept()
        browser_handler = threading.Thread(target=handle, args=(browser, addr, ))
        browser_handler.start()

    
if __name__ == "__main__":
    start()