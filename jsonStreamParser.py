#!/usr/bin/python

import sys
import re

class State:
    def __init__(self):
        self.brkts = 0
        self.delim = ":"
        self.sep = "."
        self.lastField = ""
        self.lastVal = ""
        self.F = [self.lastField]
        self.rows = 0
        self.lines = 0
        self.acceptField = True
        self.dqc = 0
        self.sqc = 0
        self.rowDict = {}

    def clear(self, force=False):
        if (force or (self.checkState() >= 0 and self.checkQuotes())):
            self.brkts = 0
            self.dqc = 0
            self.sqc = 0
            self.lastField = ""
            self.lastValue = ""
            self.F = [self.lastField]
            self.acceptField = True

    def printState(self):
        print "State: rows: ", self.rows, " lines: ", self.lines, " brkts: ", self.brkts, " fields: ", self.F

    def printRow(self):
        for k in self.rowDict.keys():
            print self.rows, self.delim, k, self.delim, self.rowDict[k]

    def checkState(self):
        if (0 > self.brkts):
            print "State: Error ... extra closing brackets at: "
            self.printState()
            return -1
        return (self.brkts * (len(self.F) - 1)) # should return zero if everything is fine

    def addRow(self):
        self.rows = self.rows + 1

    def openBracket(self):
        self.F.append(self.lastField + self.sep)
        self.lastField = self.F[self.brkts]
        self.brkts = self.brkts + 1
        self.acceptNewField()
        self.printState()

    def closeBracket(self):
        self.brkts = self.brkts - 1
        self.F.pop()
        self.lastField = self.F[self.brkts - 1]
        self.printState()

    def addField(self, field):
        if (self.acceptField):
            tfield = field.strip()
            self.F[self.brkts] = self.lastField + self.sep + tfield
            self.acceptField = False
            self.lastVal = tfield
            self.printState()
            return True
        return False

    def addValue(self,val):
        self.lastVal = val.strip()
        if (len(self.lastVal) > 0):
            print "Adding ", self.F[self.brkts] , " : ",  self.lastVal
            self.rowDict[self.F[self.brkts]] = self.lastVal
            self.lastVal = ""

    def acceptNewField(self):
        self.acceptField = True

    def updateQuotes(self, myChar):
        if ("\"" == myChar):
            if (self.dqc == 1):
                self.dqc = 0
                self.sqc = 0 # precendence
            else:
                self.dqc = 1
        if ("\'" == myChar):
            if (self.sqc == 1):
                self.sqc = 0
            else:
                self.sqc = 1

    def checkQuotes(self):
        if (self.dqc % 2 == 0 and self.sqc % 2 == 0):
            return True
        return False;

def organize(line, myState):

    try:

        pf=0

        for i,c in enumerate(line):

            if (myState.checkQuotes()):

                if ("{" == c):
                    myState.openBracket()
                    pf = i + 1

                # i - 1 gives a problem so i ?
                if (myState.delim == c):
                    myState.addField(line[pf:(i)])
                    pf = i + 1
                    myState.acceptNewField()

                if ("}" == c or "," == c):
                    myState.addValue(line[pf:(i)])
                    pf = i + 1
                if ("}" == c):
                    myState.closeBracket()
                    if (myState.brkts == 0):
                        myState.addRow()
                        myState.printRow()

            if (("\"" == c or "\'" == c) and (line[i-1] != "\\" or line[i-2] == "\\")):
                myState.updateQuotes(c)

        myState.lines = myState.line + 1

    except:
        myState.printState()
        myState.clear()

def lazyRead():
    myState = State()
    for line in sys.stdin:
        organize(line, myState)

if __name__ == '__main__':
    lazyRead()
