#-*- coding: utf-8 -*-

class User(object):

    def __init__(self, nick, sock):
        self.sock = sock
        self.nick = nick

    
    def send_msg(self, msg):
        self.sock.send(msg + "\n")


    def __str__(self):
        return self.nick
