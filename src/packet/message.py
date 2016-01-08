#-*- coding: utf-8 -*-

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import json

from src.packet.type import PKT_MESSAGE
from src.packet.packet import Packet

class MessagePacket(Packet):

    def __init__(self, *args, **kwargs):
        self.__iv = str.encode("*#hello,world!#*")
        if "key" in kwargs.keys():
            self.__key = kwargs["key"]
        else:
            self.__key = None
        if "data" in kwargs.keys():
            self._data = json.loads(kwargs["data"])
            with open("./log", "a") as f:
                f.write("UNPACK: " + str(self._data) + "\n")
            if self.__key is not None:
                self._data["msg"] = self.__decrypt(self._data["msg"])
        else:
            self._data = dict()
            self._data["type"] = PKT_MESSAGE 
            if self.__key is not None:
                if "keyhash" in kwargs.keys():
                    self.__keyhash = kwargs["keyhash"]
                    self._data["keyhash"] = self.__keyhash
                    self._data["msg"] = self.__encrypt(kwargs["msg"])

    def unpack(self):
        return self._data["user"], self._data["msg"] 

    @property
    def keyhash(self):
        return self._data["keyhash"]
    
    @property
    def user(self):
        if "user" in self._data.keys():
            return self._data["user"]
        else:
            return None

    @user.setter
    def user(self, user):
        self._data["user"] = str(user)

    def __encrypt(self, msg):
        enc = AES.new(self.__key, AES.MODE_CBC, self.__iv)
        return b64encode(enc.encrypt(self.__pad(msg)))

    def __decrypt(self, msg):
        dec = AES.new(self.__key, AES.MODE_CBC, self.__iv)
        return self.__unpad(dec.decrypt(b64decode(msg)))

    def __pad(self, data):
        to_pad = 16 - (len(data) % 16)
        return data + chr(to_pad) * to_pad

    def __unpad(self, data):
        return data[:-ord(data[-1])]

