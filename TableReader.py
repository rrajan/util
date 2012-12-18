import numpy as np

class TableReader():

    def __init__(self):
        self.fname  = ""
        self.rnames = ""
        self.cnames = ""
        self.dat    = 0

    def read(self, fname, hasRowName=True, hasColName=True, delim=","):
        self.fname = fname
        mat = np.genfromtxt(fname, delimiter=delim, skiprows=0,dtype=None)
        self.rnames = mat[:,0]
        self.cnames = mat[0,:]
        r,c = mat.shape
        self.dat = np.array(mat[1:r,1:c], dtype=np.float32)
