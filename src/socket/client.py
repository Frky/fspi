#-*- coding: utf-8 -*-

import socket

from src.socket.default import DEFAULT_PORT

# TODO parse config file for client
# TODO authentication of clients

class Client(object):

    def __init__(self, port=DEFAULT_PORT):
        self.nick = nick
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui = CommandLineUI()
