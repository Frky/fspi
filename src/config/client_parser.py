#-*- coding: utf-8 -*-


from src.config.parser import Parser


class ClientParser(object):

    req_fields =    {
                        "general":  {
                                        "nick": "",
                                },
                        "server":   {
                                        "addr": "",
                                        "port": "",
                            },
                        "comptoir": {
                                        "cid": "",
                                        "key": "",
                            },
                    }


    def __init__(self, path):
        """
            Parse a configuration file for client

            @param path     Path to the config file.

        """
        self.path = path


    def parse(self):
        p = Parser(self.path, True)
        p.parse()
        p.check_required_fields(ClientParser.req_fields)
        return p.config

