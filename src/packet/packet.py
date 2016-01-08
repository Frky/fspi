#-*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import json

class Packet(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.__data = None
        self.__type = None

    def pack(self):
        with open("./log", "a") as f:
            f.write("PACK: " + str(self._data) + "\n")
        return json.dumps(self._data)

    @abstractmethod
    def unpack(self):
        pass

    @staticmethod
    def get_type(jsdata):
        # TODO handle exception
        return json.loads(jsdata)["type"]

