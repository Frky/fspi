#-*- coding: utf-8 -*-

from random import choice

from test import Test
from src.comptoir import Comptoir
from src.exception.comptoir_already_exists import ComptoirAlreadyExistsException
from src.exception.already_connected import AlreadyConnectedException

class ComptoirTest(Test):

    def __init__(self):
        super(ComptoirTest, self).__init__()
        self.name = "Comptoir"


    def test_id(self):
        # First, let's test the generation of ids
        for i in xrange(1000):
            c = Comptoir()
        self.ok("creation")
        # Second, let's use our own ids and see what happen ...
        # If no collision:
        id_set = ['a']
        try:
            for i in xrange(1000):
                new_id = id_set[0]
                while new_id in id_set:
                    new_id = "".join([choice(Comptoir.charset) for x in xrange(Comptoir.id_len)])
                cid = Comptoir(new_id).id
                assert cid == new_id
                assert cid not in id_set
                id_set.append(cid)
            self.ok("id generation")
        except AssertionError:
            self.ko("id generation")
        # And then let's try collisions
        try:
            # This call should raise an exception
            Comptoir(id_set[1])
            self.ko("id collision")
        except ComptoirAlreadyExistsException:
            self.ok("id collision")


    def test_connect(self):
        # Create a single comptoir
        c = Comptoir()
        # Test connection of a single user
        try:
            c.connect("yo")
            self.ok("single connection")
        except Exception:
            self.ko("single connection")
        # Test connection of other users
        try:
            for i in xrange(1000):
                c.connect("{0}".format(i))
            self.ok("multiple connections")
        except Exception:
            self.ko("multiple connections")
        # Test single user connected on two comptoirs
        foo = Comptoir()
        bar = Comptoir()
        try:
            foo.connect("yo")
            bar.connect("yo")
            self.ok("connetion on multiple comptoirs")
        except Exception:
            self.ko("connetion on multiple comptoirs")
        # Test single user multiple connections on the same comptoir
        try:
            # This line should raise an exception
            foo.connect("yo")
            self.ko("same user connected twice")
        except AlreadyConnectedException:
            self.ok("same user connected twice")


    def test_disconnect(self):
        raise NotImplemented


    def run(self):
        self.start()
        self.test_id()
        self.test_connect()
        self.test_disconnect()
        self.stop()

