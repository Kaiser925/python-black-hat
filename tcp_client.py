import socket

target_host = "0.0.0.0"
target_port = 9999

# Create socket object.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to client.
client.connect((target_host, target_port))

# Send datas to server.
client.send(bytes("ABCD", encoding="utf8"))

# Recive datas from server.
response = client.recv(4096)

print(bytes.decode(response))