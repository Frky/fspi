#-*- coding: utf-8 -*-

import json

from src.packet.type import PKT_QUIT
from src.packet.packet import Packet

class QuitPacket(Packet):

    def __init__(self, *args, **kwargs):
        self._data = dict()
        self._data["type"] = PKT_QUIT


    def unpack(self):
        return None
