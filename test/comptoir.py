#-*- coding: utf-8 -*-

from random import choice, shuffle

from test import Test
from src.chat.comptoir import Comptoir
from src.exception.comptoir_already_exists import ComptoirAlreadyExistsException
from src.exception.already_connected import AlreadyConnectedException
from src.exception.not_connected import NotConnectedException


class UserForComptoirTest(object):
    def __init__(self, nick):
        self.nick = nick
        self.cid = list()
    def send_msg(self, msg):
        pass


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
            c.connect(UserForComptoirTest("yo"))
            self.ok("single connection")
        except Exception as e:
            self.ko("single connection")
        # Test connection of other users
        try:
            for i in xrange(100):
                c.connect(UserForComptoirTest("{0}".format(i)))
            self.ok("multiple connections")
        except Exception as e:
            self.ko("multiple connections")
        # Test single user connected on two comptoirs
        foo = Comptoir()
        bar = Comptoir()
        yo = UserForComptoirTest("yo")
        try:
            foo.connect(yo)
            bar.connect(yo)
            self.ok("connetion on multiple comptoirs")
        except Exception:
            self.ko("connetion on multiple comptoirs")
        # Test single user multiple connections on the same comptoir
        try:
            # This line should raise an exception
            foo.connect(yo)
        except AlreadyConnectedException:
            self.ok("same user connected twice")


    def test_disconnect(self):
        # Creation of two comptoirs for tests
        foo = Comptoir()
        bar = Comptoir()
        # Creation of two users
        yo = UserForComptoirTest("yo")
        lo = UserForComptoirTest("lo")
        # Try to connect and deconnect a user from a comptoir
        try:
            foo.connect(yo)
            foo.disconnect(yo)
            self.ok("single connection/disconnection")
        except Exception:
            self.ko("single connection/disconnection")
        # Try to connect and deconnect successively one user
        try:
            for i in xrange(1000):
                foo.connect(yo)
                foo.disconnect(yo)
            self.ok("multiple connections/disconnections from one user")
        except Exception:
            self.ko("multiple connections/disconnections from one user")
        # Try to connect two users and disconnect them in the same order
        try:
            foo.connect(yo)
            foo.connect(lo)
            foo.disconnect(yo)
            foo.disconnect(lo)
            self.ok("two users connection/disconnection")
        except Exception:
            self.ko("two users connection/disconnection")
        # Try to connect two users and disconnect them in revert order
        try:
            foo.connect(yo)
            foo.connect(lo)
            foo.disconnect(lo)
            foo.disconnect(yo)
            self.ok("two users connection/disconnection - reverse order")
        except Exception:
            self.ko("two users connection/disconnection - reverse order")
        # Connect and disconnect a lot of users
        try:
            u = list()
            for i in xrange(100):
                u.append(UserForComptoirTest(str(i)))
                foo.connect(u[-1])
            for i in xrange(len(u)):
                foo.disconnect(u[i])
            self.ok("multiple users connection/disconnection")
        except Exception:
            self.ko("multiple users connection/disconnection")
        # Connect and disconnect a lot of users in shuffle order
        try:
            u = list()
            for i in xrange(100):
                u.append(UserForComptoirTest(str(i)))
                foo.connect(u[-1])
            shuffle(u)
            for i in xrange(len(u)):
                foo.disconnect(u[i])
            self.ok("multiple users connection/disconnection - shuffle order")
        except Exception as e:
            self.ko("multiple users connection/disconnection - shuffle order")
        # Disconnect a non-connected user
        try:
            # This line should raise an exception
            foo.disconnect(UserForComptoirTest("pwd"))
            self.ko("disconnect a non-connected user")
        except NotConnectedException:
            self.ok("disconnect a non-connected user")
        # Disconnect an already disconnected user
        try:
            foo.connect(yo)
            foo.disconnect(yo)
            # This line should raise an exception
            foo.disconnect(yo)
            self.ko("disconnect twice the same user")
        except NotConnectedException:
            self.ok("disconnect twice the same user")
        # Connect a user and disconnect another one
        try:
            foo.connect(yo)
            # This line should raise an exception
            foo.disconnect(lo)
            self.ko("disconnect the wrong user")
        except NotConnectedException:
            self.ok("disconnect the wrong user")
        finally:
            foo.disconnect(yo)
        # Connection and disconnection on one comptoir, then on another one
        try:
            foo.connect(yo)
            foo.disconnect(yo)
            bar.connect(yo)
            bar.disconnect(yo)
            self.ok("connection/disconnection on two comptoirs")
        except Exception as e:
            self.ko("connection/disconnection on two comptoirs")
        # Connection on two comptoirs and disconnection in same order
        try:
            foo.connect(yo)
            bar.connect(yo)
            foo.disconnect(yo)
            bar.disconnect(yo)
            self.ok("connection/disconnection on two comptoirs in the same time")
        except Exception as e:
            self.ko("connection/disconnection on two comptoirs in the same time")
        # Connection on two comptoirs and disconnection in reverse order
        try:
            foo.connect(yo)
            bar.connect(yo)
            bar.disconnect(yo)
            foo.disconnect(yo)
            self.ok("connection/disconnection on two comptoirs in the same time - reverse order")
        except Exception as e:
            self.ko("connection/disconnection on two comptoirs in the same time - reverse order")
        # Connection on one comptoir and disconnection from another
        try:
            foo.connect(yo)
            # This line should throw an exception
            bar.disconnect(yo)
            self.ko("disconnect user form the wrong comptoir")
        except NotConnectedException:
            self.ok("disconnect user form the wrong comptoir")


    def run(self):
        self.start()
        self.test_id()
        self.test_connect()
        self.test_disconnect()
        self.stop()

