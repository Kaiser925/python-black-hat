import threading
import paramiko
import subprocess
import sys


def ssh_cmd(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))

    return


def main():
    if len(sys.argv[1:]) != 4:
        print("Usage: ./bhssh_cmd.py [ip] [user] [passwd] [command]")
        print("Example: ./bhssh_cmd.py 127.0.0.1 user pa55wd ls")
        sys.exit(0)

    ip = sys.argv[1]
    user = sys.argv[2]
    passwd = sys.argv[3]
    command = sys.argv[4]

    ssh_cmd(ip, user, passwd, command)


if __name__ == "__main__":
    main()
