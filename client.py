#!/usr/bin/env python3.6

import select
import socket
import sys
import os

if len(sys.argv) < 2:
    print("usage: ./s-chat_client [server ip addr]")
    sys.exit()


#if os.path.isfile("~/.s-chat.conf"):
#    with open("~/.s-chat.conf") as f:
#        line = ""
#        while not line:
#            line = f.readline()


#else:
    
#    name = input("Hi! Tell me your name: ")
#    print(f"Hello {name}!")
    
#    with open("~/.s-chat.conf", w+) as f:
#        f.write("name : " + name)



PORT = 28900
SERVER_IP = sys.argv[1]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(2)

try:
    client_socket.connect((SERVER_IP, PORT))
except:
    print(f"Unable to connect to {SERVER_IP}")
    sys.exit()

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
            message = sys.stdin.readline()
            client_socket.send(message.encode("utf-8"))




            




