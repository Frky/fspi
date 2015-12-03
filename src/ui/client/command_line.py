#-*- coding=: utf-8 -*_

import curses
import sys

class ChatBox(object):

    def __init__(self, size, offset):
        self.content = list()
        self.size = size
        self.offset = offset
        self.screen = curses.newwin(size[0], size[1], offset[0], offset[1])


    def add_line(self, line):
        self.content.append(line)
        self.refresh()


    def pad(self, line):
        return line + " " * (self.size[1] - len(line)) 


    def __get_content(self):
        return [self.pad(line) for line in self.content[-self.size[0]:]]


    def refresh(self):
        for i, line in enumerate(self.__get_content()):
            self.screen.addstr(i, 0, line)
        self.screen.refresh()


class Prompter(object):
    
    def __init__(self, size, offset, prompt):
        self.size = size
        self.offset = offset
        self.prompt = prompt
        self.screen = curses.newwin(size[0], size[1], offset[0], offset[1])
        self.screen.hline(0, 0, '_', self.size[1])
        self.screen.addstr(self.size[0] - 1, 0, self.prompt)


    def get_input(self):
        inp = ""
        while inp == "":
            inp = self.screen.getstr(self.size[0] - 1, len(self.prompt))
        # Flush line
        self.screen.addstr(self.size[0] - 1, len(self.prompt), " " * (self.size[1] - 1 - len(self.prompt)))
        self.screen.refresh()
        # Return user input
        return inp

    

class CommandLineUI(object):

    def __init__(self, user, cid):
        self.user = user
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.chatbox = ChatBox((self.size[0] - 2, self.size[1]), (0, 0))
        self.prompter = Prompter((2, self.size[1]), (self.size[0] - 2, 0), "{0} # ".format(cid))


    def close(self):
        curses.endwin()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.flush()


    def get_input(self):
        return self.prompter.get_input()


    def new_msg(self, msg):
        self.chatbox.add_line(msg)

