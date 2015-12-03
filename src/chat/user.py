#-*- coding: utf-8 -*-

from src.socket.default import ACK

class User(object):

    def __init__(self, nick, sock):
        self.sock = sock
        self.nick = nick
        self.cid = list()

    
    def send_msg(self, msg):
        self.sock.send(msg + "\n")


    def send_ack(self):
        self.sock.send(ACK)


    def __str__(self):
        return self.nick


