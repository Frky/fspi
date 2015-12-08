#-*- coding: utf-8 -*-

import socket, ssl
import thread
import json

from src.socket.default import DEFAULT_PORT, ACK
from src.chat.chat import Chat
from src.chat.user import User

# TODO parse config file for server
# TODO add log file of connections (IP)
# TODO authentication of clients
# TODO SSL Authentication w/ certificate (for server auth.)

class Server(object):
    """
        First and basic version of the server:
        For now, only allow to create Comptoirs

    """

    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        
        # Set SSL Context
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.verify_mode = ssl.CERT_NONE
        self.context.set_ciphers("HIGH")

        # Create socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Wrap socket through ssl
        self.sock = ssl.wrap_socket(
                                        self.sock, 
                                        server_side=True, 
                                        ciphers="HIGH", 
                                        ssl_version=ssl.PROTOCOL_TLSv1, 
                                        certfile="cert/server.crt",
                                        keyfile="cert/server.key", 
                                    )

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
        usr.nick = usr.sock.recv(1024)
        # Connect the user
        self.chat.connect(usr)
        usr.send_ack()
        # Join the comptoir
        cid = usr.sock.recv(1024)
        keyhash = usr.sock.recv(1024)
        self.chat.join(usr, cid, keyhash)
        usr.send_msg(ACK)
        quit = False
        while not quit:
            try:
                data = json.loads(usr.sock.recv(1024))
                keyhash, msg = data["keyhash"], data["msg"]
            except ValueError:
                # TODO send NOACK to client
                continue
            # TODO send ACK to client
            quit = self.chat.recved(msg, cid, usr, keyhash)
        self.chat.disconnect(usr)
        usr.sock.close()


    def __del__(self):
        self.sock.close()

