#-*- coding: utf-8 -*-

import json

from src.packet.type import PKT_DISCONNECTED
from src.packet.packet import Packet

class DisconnectedPacket(Packet):

    def __init__(self, *args, **kwargs):
        if "user" in kwargs.keys():
            self._data = dict()
            self._data["type"] = PKT_DISCONNECTED 
            self._data["user"] = str(kwargs["user"])
        elif "data" in kwargs.keys():
            self._data = json.loads(kwargs["data"])

    def unpack(self):
        return self._data["user"]

    @property
    def user(self):
        if "user" in self._data.keys():
            return self._data["user"]
        else:
            return None

