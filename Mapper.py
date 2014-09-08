#!/usr/bin/python

import numpy as np
import pandas as pd

class Mapper:

    def fuse(self, df, key_map, dtype='bool', drop_resid=False, mark_resid=False, debug=False):
        c = 0
        for k,v in key_map.itertuples():
            if (k == v): continue
            if k not in df.columns: df[k] = 0
            if v in df.columns:
                df[k] += df[v]
                del df[v]
                c += 1
                if (debug): print "DEBUG - Mapper.fuse(): fusing", v, "with", k
        if (drop_resid): self.dropResid(df, key_map)
        if (dtype == 'bool'): self.makeBinary(df)
        if (mark_resid): self.markResid(df)
        print "Mapper.fuse(): mapped", c

    def makeBinary(self, df):
        df[df > 0] = 1
        df[df < 0] = 1

    def dropResid(self, df, key_map):
        vals = []
        for k,v in key_map.itertuples(): vals.append(k)
        for v2 in df.columns:
            if v2 not in vals: del df[v2]

    def markResid(self, df):
        df['UNKNOWN'] = (df.sum(axis=1) == 0).astype(np.int)

    def remap(self, df_col, key_map, rev_map=True, mark_resid=True):
        keys = {}
        if (rev_map):
            for k,v in key_map.itertuples(): keys[v] = k
        else:
            keys = key_map

        for i,k in enumerate(df_col):
            new_val = keys.get(k, '_UNKNOWN_')
            if (mark_resid):
                df_col.iloc[i] = new_val
            else:
                if (new_val != '_UNKNOWN_'):
                    df_col.iloc[i] = new_val
