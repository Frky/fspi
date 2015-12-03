#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import errno
import socket
from time import sleep

from src.socket.client import Client
from src.exception.config_file import ConfigFileException

if len(sys.argv) < 2:
    path = "config/client/default.yaml"
else:
    path = sys.argv[1]

try:
    c = Client(path)
except ConfigFileException:
    exit()
try:
    c.connect()
except socket.error as serr:
    if serr.errno != errno.ECONNREFUSED:
        raise serr
    c.close()
    print "*** Connection refused."
    print
    sys.stdout.flush()
    exit()
c.join()
c.idle()

