import socket
import threading
import select
import display
from config import CLIENT_HOST, CLIENT_PORT, PROXY_HOST, PROXY_PORT
from socks.constants import BUFFER_SIZE, General
from socks.utils import Session, Storage
from socks.connection import connection, username_password_authenticate, username_password_register, change_password_request
from socks.cryption import CryptoRequest, CryptoReply
from cryptography.exceptions import InvalidTag

def proxy_authentication(session: Session, username, password):
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((PROXY_HOST, PROXY_PORT))
    except socket.error:
        return False

    session.sock = proxy_socket
    if connection(session) is False:
        return False

    if username_password_authenticate(session, username, password) is False:
        return False

    return True


# Mode 0 is Browser -> Client -> Proxy
# Mode 1 is Proxy -> Client -> Browser
def forward_data(src: socket.socket, dst: socket.socket, session: Session, mode):
    try:
        if mode == 0:
            data = src.recv(BUFFER_SIZE)
            if not data:
                return False
            request = CryptoRequest(session)
            message = request.to_bytes(data)
            l_message = len(message)
            dst.sendall(l_message.to_bytes(2, "big"))
            dst.sendall(message)

        else:
            bl_message = src.recv(2)
            l_message = int.from_bytes(bl_message, "big")
            message = src.recv(l_message)
            if not message:
                return False
            reply = CryptoReply(session)
            if not reply.from_bytes(message):
                return False
            dst.sendall(reply.data)

        return True
    except socket.error as e:
        print(e)


def handle(browser: socket.socket, browser_addr, storage: Storage):
    session = Session()
    proxy_status = proxy_authentication(session, storage.username, storage.password)

    if proxy_status is False:
        print(f"[ERROR] Proxy server: Connect and authenticate failed")
        return

    # If authentication succeeds, initialize session with key is password
    session.browser_addr = browser_addr
    session.key = storage.password

    # Browser uses NO AUTHENTICATION REQUIRED '\x00'
    browser_connection = browser.recv(BUFFER_SIZE)
    if not browser_connection:
        return
    # Send message to accept browser
    browser.sendall(b"\x05\x00")

    proxy = session.sock
    # Multiplex 2 sockets handle
    inputs = [browser, proxy]
    while inputs:
        readable, _, _ = select.select(inputs, [], [])
        for ready_socket in readable:
            success = False
            if ready_socket == proxy:
                success = forward_data(ready_socket, browser, session, 1)
            if ready_socket == browser:
                success = forward_data(ready_socket, proxy, session, 0)
            if not success:
                proxy.close()
                break
        if proxy.fileno() == -1:
            break


def listen_incoming(host, port, storage):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((host, port))
    client.listen(20)
    print(f"[INFO] Client start listening on {(host, port)}")
    while True:
        browser, addr = client.accept()
        browser_handler = threading.Thread(target=handle, args=(browser, addr, storage,))
        browser_handler.start()


def send_register(PROXY_HOST, PROXY_PORT, storage: Storage):
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect((PROXY_HOST, PROXY_PORT))
    except socket.error:
        return False
 
    session = Session()
    session.sock = proxy_socket
    if connection(session) is False:
        return False
 
    if username_password_register(session, storage.username, storage.password) is False:
        return False
 
    return True

def change_password(username, password):
    session = Session()
    proxy_status = proxy_authentication(session, username, password)
    
    if proxy_status is False:
        print(f"[ERROR] Proxy server: Connect and authenticate failed")
        return
    
    print("[INFO] Login successfully")
    new_password = input("[INFO] Enter new password: ")
    status = change_password_request(session, username, password, new_password)
    if status is False:
        print("[INFO] Change password failed")
        return
    
    print("[INFO] Change password successfully")
    return True
    
 
def start():
    while True:
        display.welcome()
        while True:
            picked = display.user_select()
            if picked == 0:
                return
            elif picked == 1:
                username, password = display.authenticate_input()
                if len(username) == 0 and len(password) == 0:
                    break
                storage = Storage()
                storage.username = username
                storage.password = password
                print("-------------------------FUXLOG-CLIENT------------------------")
                print("[INFO] Authentication information saved")
                print("[INFO] If authentication fails, restart and authenticate again")
                listen_incoming(CLIENT_HOST, CLIENT_PORT, storage)
           
            elif picked == 2:
                username, password = display.register_input()
                if len(username) == 0 and len(password) == 0:
                    break
                storage = Storage()
                storage.username = username
                storage.password = password
                print("-------------------------FUXLOG-CLIENT------------------------")
                print("[INFO] Register information sent")
                print("[INFO] If register fails, restart and register again")
                status = send_register(PROXY_HOST, PROXY_PORT, storage)
 
            elif picked == 3:
                username, password = display.authenticate_input()
                if len(username) == 0 and len(password) == 0:
                    break
                storage = Storage()
                storage.username = username
                storage.password = password
                print("-------------------------FUXLOG-CLIENT------------------------")
                print("[INFO] Change password")
                status = change_password(username, password)
                
               
if __name__ == "__main__":
    start()
