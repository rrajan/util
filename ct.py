import csv
from collections import OrderedDict
import numpy as np

class ContingencyTable:
    def __init__(self, fname="", header=True, primary=0, ncols=100):
        self.fname   = fname
        self.header  = header
        self.primary = primary
        self.cols    = []
        self.rowDict = None
        self.colDict = None
        self.rawDict = {}
        self.pDict   = {}
        self.pRevDict= {}
        self.nrows   = 0
        self.ncols   = ncols
        self.table   = []

        for i in range(ncols):
            self.rawDict[i] = {}

    def buildObject(self):
        self.ncols=0
        with open(self.fname, 'rb') as csvfile:
            rdr = csv.reader(csvfile)
            for idx, row in enumerate(rdr):
                if (self.header and 0 == idx):
                    self.cols = row
                else:
                    for i, c in enumerate(row):
                        if c not in self.rawDict[i]:
                            self.rawDict[i][c] = []
                            if (self.primary == i):
                                self.pDict[c] = self.nrows
                                self.nrows = self.nrows + 1
                            else:
                                self.ncols = self.ncols + 1
                        if (self.primary == i):
                            self.pRevDict[idx] = c
                        self.rawDict[i][c].append(idx) # make this array for quick indexing

    def convert(self):
        self.table = np.zeros((self.nrows, self.ncols), dtype=np.int32)
        cidx = 0
        cols = {}
        for k,v in self.rawDict.iteritems():
            if k != self.primary:
                for k2,v2 in v.iteritems():
                    cols[cidx] = self.cols[k] + "_" + `k2`
                    for val in v2:
                        self.table[ self.pDict[ self.pRevDict[val] ], cidx ] = self.table[ self.pDict[ self.pRevDict[val] ], cidx ] + 1
                    cidx = cidx + 1

        self.colDict = cols
        self.rowDict = OrderedDict(sorted(self.pDict.items(), key=lambda x:x[1]))
