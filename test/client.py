import socket


TEST_BUFFER = 4096


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1080))

client.sendall(b"\x05\x01\x00")
connection_reply = client.recv(TEST_BUFFER)

# Connect to 127.0.0.1 6000
request = b"\x05\x01\x00\x01\x7f\x00\x00\x01\x17\x70"
client.sendall(request)
reply = client.recv(8096)
if reply[1] == 0:
    while True:
        msg = input("input: ")
        client.sendall(msg.encode())
        data = client.recv(8096)
        print("Client:", data)
else:
    print("Cannot connect to target")
