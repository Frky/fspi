#-*- coding: utf-8 -*-

import thread
import socket, ssl

from src.config.client_parser import ClientParser
from src.exception.config_file import ConfigFileException
from src.exception.not_connected import NotConnectedException
from src.ui.client.command_line import CommandLineUI

# TODO parse config file for client
# TODO authentication of clients
# TODO Client UI
# TODO notify UI when connected

class Client(object):

    def __init__(self, path):
        """
            Create a client instance given a configuration file

            @param path     Path to the configuration file of the client
                            to create. Must be a valid path.

        """
        self.init = False
        # Let's parse the configuration file 
        self.cfg = ClientParser(path).parse()
        self.nick = self.cfg["general"]["nick"]
        self.server = (self.cfg["server"]["addr"], self.cfg["server"]["port"])
        self.cid = self.cfg["comptoir"]["cid"]

        # Client socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Wrapping socket for ssl
        self.sock = ssl.wrap_socket(self.sock, ciphers="HIGH")

        self.connected = False
        self.ui = CommandLineUI(self.nick, self.cid)
        self.init = True


    def connect(self):
        self.sock.connect((self.server))
        self.sock.send(self.nick + "\n")
        # TODO HANDLE ACK CORRECTLY
        self.sock.recv(1024)
        self.connected = True


    def disconnect(self):
        self.sock.close()
        self.ui.close()
        self.connected = False


    def join(self, cid=None):
        """
            Require connected

        """
        if not self.connected:
            raise NotConnectedException
        self.sock.send(self.cid + "\n")
        # TODO other way to check the ACK
        self.sock.recv(1024)


    def send(self):
        while True:
            data = self.ui.get_input()
            self.sock.send(data + "\n")


    def close(self):
        self.ui.close()


    def idle(self):
        """
            Require connected

        """
        if not self.connected:
            raise NotConnectedException
        t = thread.start_new_thread(self.send, ())
        try:
            while True:
                data = self.sock.recv(1024)
                if len(data) == 0:
                    #TODO CHANGE THIS
                    raise NotConnectedException
                self.ui.new_msg(data)
        except NotConnectedException:
            self.disconnect()

    
    def __del__(self):
        if self.init:
            self.ui.close()

