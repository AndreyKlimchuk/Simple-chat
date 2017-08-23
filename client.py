#!/usr/bin/env python3.6

from tkinter import *
import argparse
import select
import socket
import sys
import os
import re

class   SChatClient:

    def __init__(self, server_address):
        
        self.server_address = server_address
        self.nickname = self.get_nickname()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_server()
        self.setup_gui()


    def connect_server(self):

        try:
            self.socket.connect(self.server_address)
        except:
            print(f"Unable to connect to {self.server_address}")
            self.finish()
        self.socket.sendall(self.nickname.encode("utf-8"))


    def setup_gui(self):

        """ Main window """
        self.root = Tk()
        self.root.title('Simple-chat')
        self.root.resizable(0, 0)
        self.root.after(10, self.check_incoming) 

        """ Log """
        self.log = Text(self.root, width=50,  height=15, font=(30))
        self.log.grid(row=0, column=0)
        self.log.config(state=DISABLED)

        """ Log scrollbar """
        self.log_sb = Scrollbar(self.root)
        self.log_sb.grid(row=0, column=1, sticky=NS)
        self.log_sb['command'] = self.log.yview
        self.log['yscrollcommand'] = self.log_sb.set

        """ Message field """
        self.msg = Text(self.root, width=50, height=4, font=(30))
        self.msg.grid(row=1, column=0)
        self.msg.bind('<Return>', self.send_message)
        self.msg.focus_set()

        """ Message scrollbar """
        self.msg_sb = Scrollbar(self.root)
        self.msg_sb.grid(row=1, column=1, sticky=NS)
        self.msg_sb['command'] = self.msg.yview
        self.msg['yscrollcommand'] = self.msg_sb.set


    def run(self):

        self.root.mainloop()


    def check_incoming(self):

        r, w, e = select.select((self.socket,), [], [], 0)
        if self.socket in r:
            self.receive_message()
        self.root.after(10, self.check_incoming)


    def send_message(self, event):

        message = self.msg.get(1.0, END).strip()
        if message:
            self.display_message(f"[Me]: {message}\n")
            self.socket.sendall(message.encode("utf-8"))
        self.msg.delete(1.0, END)


    def receive_message(self):

        message = self.socket.recv(4096).decode("utf-8")
        if not message:
            self.finish()
        else:
            self.display_message(message + '\n')


    def display_message(self, message):

        self.log.config(state=NORMAL)
        self.log.insert(END, message)
        self.log.see(END)
        self.log.config(state=DISABLED)


    def get_nickname(self):

        with open(".s-chat.conf", "a+") as f:
            f.seek(0)
            m = re.search("name\s*:\s*[^\s]+", f.read())
            if not m:
                name = self.ask_nickname(f)
            else:
                name = m.group(0).split(':', 1)[1].strip()[:12]
        return name


    def ask_nickname(self, conf_file):

        print("Hi! Welcome to simple-chat!")
        while True:
            name = input("Tell me who you are: ")
            if not name:
                continue
            elif len(name) > 16:
                print("Please, enter shorter name! (max 12 symbols)")
            else: 
                break
        conf_file.write(f"\nname: {name}\n")
        return name


    def finish(self):

        self.socket.close()
        os._exit(0)


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser("Simple-chat server", conflict_handler="resolve")
    parser.add_argument('-h', default='localhost', help='host to connect')
    parser.add_argument('-p', default=28900, type=int, help='port to connect')
    server_address = tuple(vars(parser.parse_args()).values())

    client = SChatClient(server_address)
    client.run()

