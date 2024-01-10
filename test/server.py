import socket


TEST_BUFFER = 4096


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 1080))
server.listen(5)

print(f"Server listening on {1080}")
client, addr = server.accept()

data = client.recv(TEST_BUFFER)
print(data)
client.sendall(b'\x05\x00')

data1 = client.recv(TEST_BUFFER)
print("data1", data1)
client.sendall(b'\x05\x00\x00\x01\x7f\x00\x00\x01\x13\x88')
client.sendall(b"200 Command okay\r\n")

data = client.recv(TEST_BUFFER)
print("data2", data)
client.sendall(b"234 AUTH TLS successful\r\n")

data = client.recv(TEST_BUFFER)
print("data3", data)