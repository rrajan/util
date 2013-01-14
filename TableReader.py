import numpy as np
import types

class TableReader():

    def __init__(self):
        self.fname  = ""
        self.rnames = ""
        self.cnames = ""
        self.dat    = 0

    def read(self, fname, hasRowName=False, hasColName=False, delim=",", comments=types.NoneType, dtype=np.float32):
        self.fname = fname
        mat = np.genfromtxt(fname, delimiter=delim, skip_header=0, dtype=types.StringType, comments=comments)
        rstart=0
        cstart=0
        if (hasRowName):
            self.rnames = mat[:,0]
            cstart=1
        if (hasColName):
            self.cnames = mat[0,:]
            rstart=1

        self.dat = np.array(mat[rstart:,cstart:], dtype=dtype)
