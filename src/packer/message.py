#-*- coding: utf-8 -*-

import json
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

from src.packer.packer import Packer, PKR_MESSAGE

class MessagePacker(Packer):

    def __init__(self, key, keyhash):
        self.type = PKR_MESSAGE
        self.key = key
        self.keyhash = keyhash
        # Default IV for AES keys 
        self.iv = str.encode("*#hello,world!#*")


    def pack(self, msg):
        enc = AES.new(self.key, AES.MODE_CBC, self.iv)
        data = dict()
        data["type"] = self.type
        data["msg"] = b64encode(enc.encrypt(self.pad(msg)))
        data["keyhash"] = self.keyhash
        return json.dumps(data)


    def unpack(self, data):
        dec = AES.new(self.key, AES.MODE_CBC, self.iv)
        data = json.loads(data)
        user = data["user"]
        msg = self.unpad(dec.decrypt(b64decode(data["msg"])))
        with open("./log", "a") as f:
            f.write("ACK: ")
            f.write(str(data))
            f.write("\n")
        return user, msg


    def pad(self, data):
        to_pad = 16 - (len(data) % 16)
        return data + chr(to_pad) * to_pad


    def unpad(self, data):
        return data[:-ord(data[-1])]


