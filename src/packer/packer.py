#-*- coding: utf-8 -*-


import json


PKR_GENERIC = 0
PKR_MESSAGE = 1


class Packer(object):

    def __init__(self):
        self.type = PKR_GENERIC


    def json(self):
        raise NotImplemented

