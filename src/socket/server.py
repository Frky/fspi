#-*- coding: utf-8 -*-

import socket
import thread

from src.socket.default import DEFAULT_PORT
from src.chat.chat import Chat
from src.chat.user import User

# TODO parse config file for server
# TODO add log file of connections (IP)
# TODO authentication of clients

class Server(object):
    """
        First and basic version of the server:
        For now, only allow to create Comptoirs

    """

    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.addr = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat = Chat()


    def idle(self):
        try:
            self.sock.bind(('', self.port))
            self.sock.listen(0)
            while True:
                # Waiting for a new connection
                csock, addr = self.sock.accept()
                # Threading the handler for the new client
                thread.start_new_thread(self.handle_connection, (csock, addr))
        # TODO change to any exception
        except Exception:
            self.sock.close()


    def handle_connection(self, csock, addr):
        # TODO log connection
        print("{0} Connection opened".format(addr[0]))
        # Wait for username
        nick = csock.recv(1024)[:-1]
        # Create a user instance
        usr = User(nick, csock)
        # Connect the user
        self.chat.connect(usr)
        cid = csock.recv(1024)[:-1]
        # Join the comptoir
        self.chat.join(usr, cid)
        usr.send_msg("Connected to {0}".format(cid))
        quit = False
        while not quit:
            quit = self.chat.recved(csock.recv(1024)[:-1], cid, usr)
        print("{0} Connection closed".format(addr[0]))
        self.chat.disconnect(usr)
        csock.close()
