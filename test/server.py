import socket


TEST_BUFFER = 4096


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 6000))
server.listen(5)

print(f"Server listening on {6000}")
client, addr = server.accept()
while True:
    data = client.recv(TEST_BUFFER)
    if not data:
        break
    print(data.decode())
    client.sendall(data)
