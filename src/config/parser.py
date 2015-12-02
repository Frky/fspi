#-*- coding: utf-8 -*-

import yaml

from src.exception.config_file import ConfigFileException

    #    req_struct = {
    #                    "pin": {
    #                                "path": "",
    #                                "pintool": {
    #                                                "arity": "",
    #                                                "type": "", 
    #                                                "couple": "",
    #                                    },
    #                            },
    #                    "log": {
    #                            "path": "",
    #                        }
    #                }
    #

# TODO log file

class Parser(object):
    """
        This class aims to parse a configuration
        file in yaml and to check the 
        required fields.

    """

    def __init__(self, path, verbose=False):
        self.cfg = None
        self.path = path
        self.verbose = verbose


    def log(self, msg):
        if self.verbose:
            print "*** {0}".format(msg)


    def parse(self):
        """
            Read a yaml file and extact configuration information

        """
        try:
            with open(self.path, 'r') as ymlfile:
                self.cfg = yaml.load(ymlfile)
        except IOError:
            self.log("File {0} not found -- aborting".format(self.path))
            raise ConfigFileException


    def check_required_fields(self, req, cfg=None):
        if cfg is None:
            cfg = self.cfg
        for section in req.keys():
            if section not in self.cfg.keys():
                self.log("{0} field not found in {1} -- aborting".format(section, self.path))
                raise ConfigFileException
            field = req[section]
            if isinstance(field, dict):
                self.check_required_fields(field, cfg[section])

