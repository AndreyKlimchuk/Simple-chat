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
        #socket.settimeout(2)

    def setup(self):

        self.setup_gui()

        try:
            self.socket.connect(self.server_address)
        except:
            print(f"Unable to connect to {self.server_address}")
            self.finish()
            
    def setup_gui(self):

        #sys.defaultencoding("utf-8")
        self.tk = Tk()
        self.text = StringVar()
        self.name = StringVar()
        self.name.set(self.nickname)
        self.text.set('')
        self.tk.title('Simple-chat')
        self.tk.geometry('400x300')
        
        self.log = Text(self.tk)
        self.nick = Entry(self.tk, textvariable=self.name)
        self.msg = Entry(self.tk, textvariable=self.text)
        self.msg.pack(side='bottom', fill='x', expand='true')
        self.nick.pack(side='bottom', fill='x', expand='true')
        self.log.pack(side='top', fill='both',expand='true')
        
        self.msg.bind('<Return>', self.send)
        self.msg.focus_set()
        self.tk.mainloop()

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
                print("Please, enter shorter name! (maximum 12 symbols)")
            else: 
                break
        conf_file.write(f"\nname: {name}\n")
        return name


    def run(self):

        self.setup()
        while True:
            r, w, e = select.select((self.socket,), [], [], 0)
            if self.socket in r:
                message = self.recieve()
                if not message:
                    self.finish()
                else:
                    self.log.insert(END, message + '\n')
                    self.log.see(END)

    def send(self, event):

        message = self.text.get().encode("utf-8")
        self.socket.sendall(message)

    def receive(self):

        return self.socket.recv(4096)

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


