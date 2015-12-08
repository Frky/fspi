#-*- coding: utf-8 -*-

import thread
import socket, ssl
from Crypto.Protocol.KDF import PBKDF2
from sha3 import sha3_256

from src.config.client_parser import ClientParser
from src.exception.config_file import ConfigFileException
from src.exception.not_connected import NotConnectedException
from src.ui.client.command_line import CommandLineUI
from src.packer.message import MessagePacker

# TODO authentication of clients
# TODO Client UI
# TODO notify UI when connected
# TODO check default IV security holes

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
        # Default IV for AES keys 
        self.iv = str.encode("*#hello,world!#*")
        # Derive an AES key from a passphrase 
        self.__key = PBKDF2(self.cfg["comptoir"]["key"], self.iv)
        self.pkr = MessagePacker(self.__key, self.keyhash)

        # Client socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Wrapping socket for ssl
        self.sock = ssl.wrap_socket(self.sock, ciphers="HIGH")

        self.connected = False
        self.ui = CommandLineUI(self.nick, self.cid)
        self.init = True


    def connect(self):
        self.sock.connect((self.server))
        self.sock.send(self.nick)
        # TODO HANDLE ACK CORRECTLY
        self.sock.recv(1024)
        self.connected = True


    def disconnect(self):
        self.sock.close()
        self.ui.close()
        self.connected = False


    @property
    def keyhash(self):
        return sha3_256(self.__key).hexdigest()


    def join(self, cid=None):
        """
            Require connected

        """
        if not self.connected:
            raise NotConnectedException
        self.sock.send(self.cid)
        self.sock.send(self.keyhash)
        # TODO other way to check the ACK
        self.sock.recv(1024)


    def send(self):
        while True:
            msg = self.ui.get_input()
            pkt = self.pkr.pack(msg)
            with open("./log", "a") as f:
                f.write("SYN: ")
                f.write(str(pkt))
                f.write("\n")
            self.sock.send(pkt)


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
                user, msg = self.pkr.unpack(data)
                self.ui.new_msg("[{0}] {1}".format(user, msg))
        except NotConnectedException:
            self.disconnect()

    
    def __del__(self):
        if self.init:
            self.ui.close()

