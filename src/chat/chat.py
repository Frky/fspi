#-*- coding: utf-8 -*-


from src.chat.comptoir import Comptoir

from src.exception.already_connected import AlreadyConnectedException
from src.exception.not_connected import NotConnectedException
from src.exception.invalid_hash import InvalidHashException


class Chat(object):
    """
        This class handles all the comptoirs and chat actions

    """

    def __init__(self):
        # Comptoirs open
        self.cmptr = dict()
        # Users connected
        self.usr = list()


    def connect(self, user):
        """
            Connect a new user to the chat.
            
            @raise AlreadyConnected if the user is already connected

        """
        if user in self.usr:
            raise AlreadyConnectedException
        print "[log] Connected: {0}".format(user)
        self.usr.append(user)


    def disconnect(self, user):
        """
            Disconnect a user from the chat.

            @raise NotConnected if the user is not connected

        """
        if user not in self.usr:
            raise NotConnectedException
        print "[log] Disconnected: {0}".format(user)
        for cid in user.cid:
            self.cmptr[cid].disconnect(user)
        self.usr.remove(user)


    def join(self, user, cid, keyhash):
        """
            Join the comptoir cid
            This function creates the comptoir if it does not
            exists, and then connect the user to the comptoir.

            @raise NotConnected if the user is not yet connected 
                    to the chat

        """
        if user not in self.usr:
            raise NotConnectedException
        if cid not in self.cmptr.keys():
            print "Creating comptoir"
            self.cmptr[cid] = Comptoir(cid, keyhash)
        self.cmptr[cid].connect(user, keyhash)

    
    def recved(self, packet, cid, user, keyhash):
        """
            Handler for the reception of a packet from user

        """
        if packet == "/quit" or packet == "":
            return True
        try:
            # Follow packet to relevant comptoir
            self.cmptr[cid].new_msg(packet, user, keyhash)
        except InvalidHashException:
            # TODO this should not be sent by Chat object ...
            user.sock.send("Message rejected: invalid hash.\n")
        return False

