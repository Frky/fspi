#!/usr/bin/python
#-*- coding: utf-8 -*-

from src.socket.server import Server

# Creation of a new server
svr = Server()

try:
    # Idle the server
    svr.idle()
except KeyboardInterrupt:
    del(svr)
    print
