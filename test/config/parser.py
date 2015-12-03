#-*- coding: utf-8 -*-

from random import choice

from src.config.parser import Parser
from test.test import Test
from src.exception.config_file import ConfigFileException

class ParserTest(Test):

    def __init__(self):
        super(ParserTest, self).__init__()
        self.name = "Parser"


    def test_init(self):
        """
            Test a few simple instanciations if the class

        """
        for i in xrange(1000):
            p = Parser("".join([choice("azertyuiopqsdfghjklmwxcvbn/") for i in xrange(choice(range(100)))]))
        self.ok("instantiation")


    def test_parse(self):
        """
            Test parsing of yaml files 

        """
        # Test the parsing of a correct file
        try:
            p = Parser("test/config/valid.yaml")
            p.parse()
            self.ok("parsing a valid file")
        except Exception:
            self.ko("parsing a valid file")

        # We are not here to test yaml package, 
        # so let's assume it does its job correctly

        # Test the parsing of a file that does not exist
        try:
            p = Parser("test/config/ghost.yaml")
            # This line should throw an exception
            p.parse()
            self.ko("parsing an inexisting file")
        except ConfigFileException:
            self.ok("parsing an inexisting file")


    def test_check(self):
        # Check a file with a depth of one
        p = Parser("test/config/depth_one.yaml")
        p.parse()
        # Positive tests
        # All fields required
        try:
            p.check_required_fields({ "foo": "", "bar": "", "foobar": ""})
            self.ok("depth one -- all fields required")
        except ConfigFileException:
            self.ko("depth one -- all fields required")
        # Only one field required
        try:
            p.check_required_fields({ "foo": ""})
            p.check_required_fields({ "bar": ""})
            p.check_required_fields({ "foobar": ""})
            self.ok("depth one -- one field required")
        except ConfigFileException:
            self.ko("depth one -- one field required")
        # Several fields required
        try:
            p.check_required_fields({ "foo": "", "bar": ""})
            p.check_required_fields({ "foo": "", "foobar": ""})
            p.check_required_fields({ "bar": "", "foobar": ""})
            self.ok("depth one -- two fields required")
        except ConfigFileException:
            self.ko("depth one -- two fields required")

        # Negative tests
        # One field required not present, zero present
        try:
            p.check_required_fields({ "FOO": ""})
            self.ko("depth one -- one required field missing")
        except ConfigFileException:
            self.ok("depth one -- one required field missing")
        # One field required not present, one present
        try:
            p.check_required_fields({ "FOO": "", "bar": ""})
            self.ko("depth one -- one required field missing, one present")
        except ConfigFileException:
            self.ok("depth one -- one required field missing, one present")
        # One field required not present, two present
        try:
            p.check_required_fields({ "FOO": "", "bar": "", "foobar": ""})
            self.ko("depth one -- one required field missing, two present")
        except ConfigFileException:
            self.ok("depth one -- one required field missing, two present")
        # Two fields required not present, zero present
        try:
            p.check_required_fields({ "FOO": "", "BAR": "", "foobar": ""})
            self.ko("depth one -- two required fields missing")
        except ConfigFileException:
            self.ok("depth one -- two required fields missing")
        # Two fields required not present, one present
        try:
            p.check_required_fields({ "FOO": "", "BAR": "", "foobar": ""})
            self.ko("depth one -- two required fields missing, one present")
        except ConfigFileException:
            self.ok("depth one -- two required fields missing, one present")
        # Three fields required not present
        try:
            p.check_required_fields({ "FOO": "", "BAR": "", "FOOBAR": ""})
            self.ko("depth one -- all required fields missing")
        except ConfigFileException:
            self.ok("depth one -- all required fields missing")

        # Check a file with a depth of two
        # Positive tests
        # Negative tests


        # Check a file with a depth of three
        # Positive tests
        # Negative tests


    def run(self):
        self.start()
        self.test_init()
        self.test_parse()
        self.test_check()
        self.stop()

