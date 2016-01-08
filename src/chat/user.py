#-*- coding: utf-8 -*-

from src.socket.default import ACK

class User(object):

    def __init__(self, nick, sock):
        self.sock = sock
        self.nick = nick
        self.cid = list()

    
    def send(self, pkt):
        self.sock.send(pkt.pack() + "\n")


    def send_ack(self):
        self.sock.send(ACK + "\n")


    def __str__(self):
        return self.nick


