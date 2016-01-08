#-*- coding: utf-8 -*-

from random import choice
import json

from src.packet.connected import ConnectedPacket
from src.packet.disconnected import DisconnectedPacket

from src.exception.already_connected import AlreadyConnectedException
from src.exception.not_connected import NotConnectedException
from src.exception.comptoir_already_exists import ComptoirAlreadyExistsException
from src.exception.invalid_hash import InvalidHashException


class Comptoir(object):

    charset = "azertyuiopmlkjhgfdsqwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN"
    id_len = 10
    cid = list()

    def __init__(self, id="", keyhash=""):
        """
            Creation of a new comptoir. If no id is specified, 
            a random id is generated.

            @param id   required id for the comptoir (optional)

            @raise  ComptoirAlreadyExists if the specified id match
                    an existing comptoir

        """

        # If an id is specified
        if id != "":
            # Check if already used
            if id in Comptoir.cid:
                raise ComptoirAlreadyExistsException
            # Otherwise, use it as the comptoir id
            else:
                self.__id = id
        else:
            # Generate random id for the comptoir 
            self.__id = "".join([choice(Comptoir.charset) for x in xrange(Comptoir.id_len)])
        # Hash of the comptoir key
        self.__keyhash = keyhash
        # List of connected users
        self.__connected = list()
        Comptoir.cid.append(self.__id)

    def is_ciphered(self):
        return self.__keyhash != ""


    @property
    def id(self):
        """
            Getter for the comptoir id

        """
        return self.__id 


    def check_hash(self, keyhash):
        if self.is_ciphered() and self.__keyhash != keyhash:
            raise InvalidHashException


    def connect(self, user, keyhash=""):
        """
            Connect a new user to the comptoir.
            First test if the user is already connected
            (in this case, throw AlreadyConnected)

        """
        if user in self.__connected:
            raise AlreadyConnectedException
        self.check_hash(keyhash)
        self.__connected.append(user)
        user.cid.append(self.id)
        for u in self.__connected:
            if u != user:
                u.send(ConnectedPacket(user=user))


    def disconnect(self, user):
        """
            Disconnect a user from the comptoir.
            If the user is not connected, throw NotConnectedException.

        """
        if user not in self.__connected:
            raise NotConnectedException
        self.__connected.remove(user)
        user.cid.remove(self.id)
        for u in self.__connected:
            if u != user:
                u.send(DisconnectedPacket(user=user))


    def new_msg(self, pkt, user):
        """
            Handler of new messages on comptoir
            Check the hash of the comptoir key first.
            Forward the message to all users connected.

            @raise NotConnected if user is not connected 
                    to the comptoir

        """
        if user not in self.__connected:
            raise NotConnectedException
        self.check_hash(pkt.keyhash)
        # Overwrite user field to ensure it is correct
        pkt.user = user
        for u in self.__connected:
            u.send(pkt)

