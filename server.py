#!/usr/bin/env  python3.6

import socketserver
import select
import argparse

class   SChatServer(socketserver.ThreadingTCPServer):

    allow_reuse_address = True

    def __init__(self, server_adress, RequestHandlerClass):
        """
        Call TCPServer class's constructor and create set to store
        all new connections.
        """

        super().__init__(server_adress, RequestHandlerClass, True)
        self.clients = set()

    def add_client(self, client_socket):

        self.clients.add(client_socket)

    def remove_client(self, client_socket):

        self.clients.remove(client_socket)

    def broadcast(self, sender, data):
        """
        Encode message if it's not in binary format and send it to
        all clients, except sender.
        """

        if type(data) is str:
            data = data.encode("utf-8")
        for client in self.clients:
            if client is not sender:
                client.sendall(data)

class   NewClientHandler(socketserver.StreamRequestHandler):

    def setup(self):
        """
        Get the client's nickname, which he sends immediately after
        connection is established, save client's socket in set, and
        notify other clients about new participant.
        """

        super().setup()
        self.nickname = self.get_data().decode("utf-8")
        self.server.add_client(self.request)
        message = f"{self.nickname} entered chat-room!"
        self.server.broadcast(self.request, message)

    def handle(self):
        """
        Wait when client's socket become readable in nonblocking manner,
        get message, process and send it to other clients.
        """

        while True:
            r, w, e = select.select((self.request,), [], [], 0)
            if self.request in r:
                data = self.get_data()
                if not data:
                    break
                data = self.process_data(data)
                self.server.broadcast(self.request, data)


    def finish(self):
        """
        Notify clients that participant left room and
        removes his socket from set.
        """

        message = f"{self.nickname} left chat-room!"
        self.server.broadcast(self.request, message)
        self.server.remove_client(self.request)
        super().finish()

    def get_data(self):

        return self.request.recv(4096)

    def process_data(self, data):
        """ Prepend message with nickname """

        data = data.decode("utf-8")
        data = '[' + self.nickname + ']: ' + data;
        return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Simple-chat server")
    parser.add_argument('-h', default='localhost', help='host to run server on')
    parser.add_argument('-p', default=28900, type=int, help='port to run server on')
    server_address = patser.parse_args()
    server = SChatServer(server_address, NewClientHandler)
    server.serve_forever()





