import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

# Set the maximum number of connections
server.listen(5)

print(f"[*] Listen on {bind_ip}:{bind_port}")

def handle_client(client_socket:socket):
    req = client_socket.recv(1024)
    print(f"[*] Recived:{bytes.decode(req)}")
    client_socket.send(bytes("ACK!", encoding="utf8"))
    client_socket.close()

while True:
    client, addr = server.accept()

    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

    client_handle = threading.Thread(target=handle_client, args=(client,))
    client_handle.start()