#!/usr/bin/env  python3.6

import socket
import select
import sys

HOST = ''
PORT = 28900

class   Chat_server:

    def __init__(self):

        self.main_sock = socket.socket(socket.AF_INET,
                                       socket.SOCK_STREAM)
        self.main_sock.setsockopt(socket.SOL_SOCKET,
                                  socket.SO_REUSEADDR, 1)
        self.main_sock.bind((HOST, PORT))
        self.socket_list = [self.main_sock]

    def run(self):

        self.main_sock.listen(10)
        print("I'm listening ...")

        while True:

            readable, __, __ = \
                select.select(self.socket_list, [], [], 0)

            for sock in readable:

                if sock == self.main_sock:

                    print("New incomming connection")
                    client_sock, addr = self.main_sock.accept()
                    self.socket_list.append(client_sock)
                    self.send_to_all(self.main_sock, b"somebody entered chat-room")

                else:

                    message = sock.recv(1024)

                    if not message:

                        if sock in self.socket_list:
                            print("removed")
                            self.socket_list.remove(sock)
                        self.send_to_all(self.main_sock, b"somebody has gone offline")

                    else:

                        self.send_to_all(sock, message)


    def send_to_all(self, sender, message):

        for sock in self.socket_list:

            if sock != self.main_sock and sock != sender:

                try:
                    sock.send(message)
                except:

                    if sock in self.socket_list:
                        self.socket_list.remove(sock)


if __name__ == "__main__":

    server = Chat_server()
    server.run()




