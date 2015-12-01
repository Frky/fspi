#-*- coding: utf-8 -*-

class Test(object):

    def __init__(self):
        self.err = 0
        self.tot = 0
        self.name = ""


    def ok(self, tname):
        self.tot += 1
        print "[OK] {0}".format(tname)


    def ko(self, tname):
        self.err += 1
        self.tot += 1
        print "[KO] {0}".format(tname)


    def start(self):
        self.err = 0
        self.tot = 0
        print "***** Running tests for {0} *****".format(self.name)


    def stop(self):
        if self.err == 0:
            print "[**] ALL OK."
            print
        elif self.err == 1:
            print "[**] 1 ERROR"
            print
        else:
            print "[**] {0} ERRORS".format(self.err)
            print

