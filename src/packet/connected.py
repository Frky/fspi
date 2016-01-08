#-*- coding: utf-8 -*-

import json

from src.packet.type import PKT_CONNECTED
from src.packet.packet import Packet

class ConnectedPacket(Packet):

    def __init__(self, *args, **kwargs):
        if "user" in kwargs.keys():
            self._data = dict()
            self._data["type"] = PKT_CONNECTED 
            self._data["user"] = str(kwargs["user"])
        elif "data" in kwargs.keys():
            self._data = json.loads(kwargs["data"])
        else:
            self._data = None

    def unpack(self):
        return self._data["user"]

    @property
    def user(self):
        if "user" in self._data.keys():
            return self._data["user"]
        else:
            return None

