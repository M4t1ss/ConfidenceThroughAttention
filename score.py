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
    parser.add_argument("-a", "--alignments",  required=True, action="store", dest="ali", help="Alignment file")

    # only required for neuralmonkey alignments
    parser.add_argument("-f", "--framework",  required=False, choices=['Nematus', 'NeuralMonkey'], action="store", dest="frm", help="Nematus or NeuralMonkey")
    parser.add_argument("-s", "--source",  required=False, action="store", dest="src", help="Neural Monkey source sentence subword units")
    parser.add_argument("-t", "--target",  required=False, action="store", dest="trg", help="Neural Monkey target sentence subword units")

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

    if args.frm == "NeuralMonkey":
        srcs = readSnts(args.src)
        tgts = readSnts(args.trg)
        alis = np.load(args.ali)
    if args.frm == "Nematus":
        (srcs, tgts, alis) = readNematus(args.ali)

    data = list(zip(srcs, tgts, alis))

    with open(args.ali + '.csv', 'w') as outfile:
        for i in range(0, len(data)):
            (src, tgt, rawAli) = data[i]
            ali = [l[:len(tgt)] for l in rawAli[:len(src)]]
            
            CP = thecode.getCP(ali)
            Ent = thecode.getEnt(ali)
            RevEnt = thecode.getRevEnt(ali)
            Mult = CP + Ent + RevEnt
            
            outfile.write(
                repr(i) + '\t' 
                + repr(CP) + '\t' 
                + repr(Ent) + '\t' 
                + repr(RevEnt) + '\t' 
                + repr(Mult) + '\n')


if __name__ == "__main__":

    args = parse_args()
    
    try:
        args.frm
    except NameError:
        outputType = "NeuralMonkey"
     
    try:
        if args.frm == "NeuralMonkey":
            check_argument("-s (source)",args.src, "NeuralMonkey")
            check_argument("-t (target)",args.trg, "NeuralMonkey")
    except IOError as e:
        sys.exit(e)

    main(args)
    

        