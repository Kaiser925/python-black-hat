import socket

target_host = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# UDP is stateless, so there is no need to connect in advance.
client.sendto(bytes("AAABBBCCC", encoding="utf8"),  (target_host, target_port))

data, addr = client.recvfrom(4096)

print(bytes.decode(data))