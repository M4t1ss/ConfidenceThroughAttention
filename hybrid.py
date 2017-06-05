# coding: utf-8

import thecode
import argparse
import sys, getopt
import numpy as np
import string
import os
from io import StringIO

def parse_args():
    """parses arguments given when program is called"""
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("-nem", "--nematus",  required=True, action="store", dest="nem", help="Nematus alignment file")
    parser.add_argument("-nm", "--neuralmonkey",  required=True, action="store", dest="nm", help="Neural Monkey alignment file")
    parser.add_argument("-s", "--source",  required=True, action="store", dest="src", help="Neural Monkey source sentence subword units")
    parser.add_argument("-t", "--target",  required=True, action="store", dest="trg", help="Neural Monkey target sentence subword units")

    return parser.parse_args()

def check_argument(arg,value,frm):
    """checks whether argument is present, raises IOError else"""

    if not value:
        raise IOError("error: {0:s} must be defined for {1:s} alignments".format(arg,frm))

def readSnts(filename):
    with open(filename, 'r') as fh:
        return [line.strip().split() for line in fh]

def readNematus(filename):
    with open(filename, 'r') as fh:
        alis = []
        tgts = []
        srcs = []
        wasNew = True
        aliTXT = ''
        for line in fh:
            if wasNew:
                if len(aliTXT) > 0:
                    c = StringIO(aliTXT)
                    ali = np.loadtxt(c)
                    ali = ali.transpose()
                    alis.append(ali)
                    aliTXT = ''
                lineparts = line.split(' ||| ')
                lineparts[1] += ' <EOS>'
                lineparts[3] += ' <EOS>'
                tgts.append(lineparts[1].strip().split())
                srcs.append(lineparts[3].strip().split())
                wasNew = False
                continue
            if line != '\n' and line != '\r\n':
                aliTXT += line
            else:
                wasNew = True
        if len(aliTXT) > 0:
            c = StringIO(aliTXT)
            ali = np.loadtxt(c)
            ali = ali.transpose()
            alis.append(ali)
            aliTXT = ''
    return srcs, tgts, alis

def main(argv):

    srcs1 = readSnts(args.src)
    tgts1 = readSnts(args.trg)
    alis1 = np.load(args.nm)
    (srcs2, tgts2, alis2) = readNematus(args.nem)

    data = list(zip(srcs1, tgts1, alis1, srcs2, tgts2, alis2))

    with open(args.nem + '.hybrid', 'w') as outfile:
        for i in range(0, len(data)):
            (src1, tgt1, rawAli1, src2, tgt2, rawAli2) = data[i]
            ali1 = [l[:len(tgt1)] for l in rawAli1[:len(src1)]]
            ali2 = [l[:len(tgt2)] for l in rawAli2[:len(src2)]]
            
            CP1 = thecode.getCP(ali1)
            Ent1 = thecode.getEnt(ali1)
            RevEnt1 = thecode.getRevEnt(ali1)
            Mult1 = CP1 + Ent1 + RevEnt1
            
            CP2 = thecode.getCP(ali2)
            Ent2 = thecode.getEnt(ali2)
            RevEnt2 = thecode.getRevEnt(ali2)
            Mult2 = CP2 + Ent2 + RevEnt2
            
            if Mult1 > -1.5 and Mult2 < -1.5:
                outfile.write(' '.join(tgt2).replace("@@ ", "").replace(" <EOS>", "") + '\n')
            elif Mult2 > -1.5 and Mult1 < -1.5:
                outfile.write(' '.join(tgt1).replace("@@ ", "") + '\n')
            elif Mult2 > Mult1:
                outfile.write(' '.join(tgt2).replace("@@ ", "").replace(" <EOS>", "") + '\n')
            else:
                outfile.write(' '.join(tgt1).replace("@@ ", "") + '\n')


if __name__ == "__main__":

    args = parse_args()

    main(args)
           