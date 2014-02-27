#!/usr/bin/python

import sys
#import re

class State:
    def __init__(self):
        self.lines = 0
        self.hist = {}

    def dump(self):
        for k,v in self.hist.iteritems():
            print k, v

    def dumpSorted(self):
        for k,v in sorted(self.hist.items(), key=lambda x: -x[1]):
            print k, v


    def add(self,val):
        self.lines = self.lines + 1
        if (val in self.hist):
            self.hist[val] += 1
        else:
            self.hist[val] = 1


def organize(line, myState):
    myState.add(line.strip())

def lazyRead():
    myState = State()
    rows = 0
    for line in sys.stdin:
        organize(line, myState)

    sys.stderr.write("Read " + `myState.lines` + " lines. Printing Counts...\n")
    myState.dumpSorted()

if __name__ == '__main__':
    lazyRead()
