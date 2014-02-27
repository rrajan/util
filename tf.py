import sys, re, time, string
import numpy as np

class TF:

    def __init__(self):
        self.tfv = 0
        self.nWords = 0
        self.vocab = 0
        self.wcs = 0
        self.mat = 0

    def buildTF(self, docs, stopVocab = list()):
        """
        Parse a document into a list of word ids and a list of counts,
        or parse a set of documents into two lists of lists of word ids
        and counts.

        Arguments: 
        docs:  List of D documents. Each document must be represented as
               a single string. (Word order is unimportant.) Any
               words in the stop vocabulary will be ignored.
        stopVocab: list of stop words

        Returns a list of dict (tf) and a dict of vocab

        The first, wordids, says what vocabulary tokens are present in
        each document. wordids[i][j] gives the jth unique token present in
        document i. (Don't count on these tokens being in any particular
        order.)

        The second, wordcts, says how many times each vocabulary token is
        present. wordcts[i][j] is the number of times that the token given
        by wordids[i][j] appears in document i.
        """
        if (type(docs).__name__ == 'str'):
            temp = list()
            temp.append(docs)
            docs = temp

        D = len(docs)

        vocab = dict()
        nWords = 0
        tf = list()
        for d in range(0, D):
            docs[d] = docs[d].lower()
            docs[d] = re.sub(r'-', ' ', docs[d])
            docs[d] = re.sub(r'^#', '', docs[d])
            docs[d] = re.sub(r'^@', '', docs[d])
            #docs[d] = re.sub(r'[^a-z ]', '', docs[d])
            docs[d] = re.sub(r' +', ' ', docs[d])
            words = string.split(docs[d])
            ddict = dict()
            for word in words:
                if (not word in stopVocab):
                    if (not word in vocab):
                        vocab[word] = nWords
                        nWords = nWords + 1
                    wordtoken = vocab[word]
                    if (not wordtoken in ddict):
                        ddict[wordtoken] = 0
                    ddict[wordtoken] += 1
            tf.append(ddict)

        self.tfv = tf
        self.vocab = vocab
        self.nWords = nWords

    def wc(self):
        wcs = dict()
        for v in self.tfv:
            for wid, wct in v.items():
                if (not wid in wcs):
                    wcs[wid] = 0
                wcs[wid] = wcs[wid] + wct

        self.wcs = wcs

    def filtTerms(self, tfmin=5, tfmax=-1):
        if (0 == self.wcs):
            self.wc()
        keys = list()
        vals = list()
        for k,v in self.wcs.items():
            if (v >= tfmin):
                if (tfmax >= tfmin):
                    if (v <= tfmax):
                        keys.append(k)
                        vals.append(v)
                else:
                    keys.append(k)
                    vals.append(v)

        return ((keys, vals))

    def tfMat(self, tfmin=5, tfmax=-1):
        keys = 0
        vals = 0
        if (tfmin > 0):
            keys, vals = self.filtTerms(tfmin, tfmax)
        else:
            self.wc()
            keys = self.wcs.keys()
            vals = self.wcs.values()

        ncols = 0
        cids = dict()
        for k in keys:
            cids[k] = ncols
            ncols += 1

        mat = list()

        rids = list()
        for i, v  in enumerate(self.tfv):
            y = np.zeros(ncols)
            for key, val in v.items():
                if (key in keys):
                    y[cids[key]] = val

            if (np.sum(y) > 0):
                rids.append(i)
                mat.append(y)

        return ((np.array(mat), keys, rids))

    def getTerms(self, ids=list()):
        if (len(ids) == 0):
            print "No IDs provided"
            return
        terms = list()
        for k,v in self.vocab.items():
            if (v in ids):
                terms.append(k)
        return terms
