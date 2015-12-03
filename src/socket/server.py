#-*- coding: utf-8 -*-

import socket
import thread

from src.socket.default import DEFAULT_PORT, ACK
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
        self.__connected = list()


    def idle(self):
        self.sock.bind(('', self.port))
        self.sock.listen(0)
        while True:
            # Waiting for a new connection
            # TODO log connection
            csock, addr = self.sock.accept()
            print("{0} Connection opened".format(addr[0]))
            # Create a new user instance
            usr = User("", csock)
            self.__connected.append(usr)
            # Threading the handler for the new client
            thread.start_new_thread(self.handle_connection, (usr,))


    def handle_connection(self, usr):
        # Wait for username
        usr.nick = usr.sock.recv(1024)[:-1]
        # Connect the user
        self.chat.connect(usr)
        usr.send_ack()
        # Join the comptoir
        cid = usr.sock.recv(1024)[:-1]
        self.chat.join(usr, cid)
        usr.send_msg(ACK)
        quit = False
        while not quit:
            quit = self.chat.recved(usr.sock.recv(1024)[:-1], cid, usr)
        self.chat.disconnect(usr)
        usr.sock.close()


    def __del__(self):
        self.sock.close()
