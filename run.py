import socket
import threading


def handle(browser: socket.socket, addr):
    print(f"[INFO] {addr} connected to HUSTSOCKS client")
    connection_request = browser.recv(4096)
    version = connection_request[0]
    method = connection_request[2]
    print(f"[INFO] {addr} version {version}, method {method}")
    browser.sendall(b"\x05\x00")

    while True:
        data = browser.recv(4096)
        if not data:
            print(f"[INFO] {addr} close connection")
            break
        print(f"[INFO] {addr} : {data}")


def run(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((host, port))
    client.listen(20)

    while True:
        browser, addr = client.accept()
        browser_handler = threading.Thread(target=handle, args=(browser, addr, ))
        browser_handler.start()

    
if __name__ == "__main__":
    run("127.0.0.1", 1080)