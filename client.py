#!/usr/bin/env python3.6

import select
import socket
import sys
import os
import re

def     get_name():

    with open(".s-chat.conf", "a+") as f:

        f.seek(0)
        m = re.search("\s*name\s*:\s*[^\s]+", f.read())

        if not m:
            print("Hi! Welcome to simple-chat!")

            while True:

                name = input("Tell me who you are: ")

                if not name:
                    continue
                elif len(name) > 16:
                    print("Please, enter shorter name! (maximum 12 symbols)")
                else: 
                    break

            f.write("\nname: %s\n" % name)

        else:

            m = m.group(0)
            name = m[m.index(':') + 1:].strip()[:12]

    return name


def client_run():

    server_ip, port = sys.argv[1], 28900

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    try:
        client_socket.connect((server_ip, port))
    except:
        print(f"Unable to connect to {server_ip}")
        sys.exit()

    client_socket.send(get_name().encode("utf-8"))

    while True:

        sockets = [sys.stdin, client_socket]
        readable, __, __ = select.select(sockets, [], [])

        for s in readable:
        
            if s == client_socket:
                message = s.recv(4096)
            
                if not message:
                    print("Connection with server lost")
                    sys.exit()
                else:
                    print(message.decode("utf-8"))

            elif s == sys.stdin:
                message = sys.stdin.readline()[:-1]
                if message:
                    client_socket.send(message.encode("utf-8"))



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: ./s-chat_client [server ip addr]")
        sys.exit()

    client_run()
            




