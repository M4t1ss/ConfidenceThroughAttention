# coding: utf-8

import thecode
import argparse
import sys, getopt
import numpy as np
import string
import os
from io import open, StringIO
import codecs
try:
    from itertools import izip
except ImportError:
    izip = zip

def parse_args():
    """parses arguments given when program is called"""
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument("-a", "--alignments",  required=True, action="store", dest="ali", help="Alignment file")

    # only required for neuralmonkey alignments
    parser.add_argument("-f", "--framework",  required=False, choices=['Nematus', 'NeuralMonkey', 'AmuNMT'], action="store", dest="frm", help="Nematus or NeuralMonkey")
    parser.add_argument("-s", "--source",  required=False, action="store", dest="src", help="Neural Monkey or AmuNMT source sentence subword units")
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
    with open(filename, 'r', encoding='utf-8') as fh:
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
                tgts.append(escape(lineparts[1]).strip().split())
                srcs.append(escape(lineparts[3]).strip().split())
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
    
def readAmu(in_file, src_file):
    with open(src_file, 'r', encoding='utf-8') as fi:
        with open(in_file, 'r', encoding='utf-8-sig') as fh:
            alis = []
            tgts = []
            srcs = []
            aliTXT = ''
            for src_line, out_line in izip(fi, fh):
                lineparts = out_line.split(' ||| ')
                lineparts[0] += ' <EOS>'
                src_line = src_line.strip() + ' <EOS>'
                tgts.append(escape(lineparts[0]).strip().split())
                srcs.append(escape(src_line).split())
                #alignment weights
                weightparts = lineparts[1].split(') | (')
                for weightpart in weightparts:
                    aliTXT += weightpart.replace('(','') + '\n'
                if len(aliTXT) > 0:
                    c = StringIO(aliTXT.replace(' ) | ',''))
                    ali = np.loadtxt(c)
                    ali = ali.transpose()
                    alis.append(ali)
                    aliTXT = ''
    return srcs, tgts, alis
    
def escape(string):
    return string.replace('"','&quot;').replace("'","&apos;")

def main(argv):

    if args.frm == "NeuralMonkey":
        srcs = readSnts(args.src)
        tgts = readSnts(args.trg)
        alis = np.load(args.ali)
    if args.frm == "Nematus":
        (srcs, tgts, alis) = readNematus(args.ali)
    if args.frm == "AmuNMT":
        (srcs, tgts, alis) = readAmu(args.ali, args.src)

    data = list(zip(srcs, tgts, alis))

    with open(args.ali + '.csv', 'w') as outfile:
        for i in range(0, len(data)):
            (src, tgt, rawAli) = data[i]
            if(len(tgt) > 1):
                ali = [l[:len(tgt)] for l in rawAli[:len(src)]]
                
                CP = thecode.getCP(ali)
                Ent = thecode.getEnt(ali)
                RevEnt = thecode.getRevEnt(ali)
                Mult = CP + Ent + RevEnt
                
                outfile.write(
                    repr(i) + u'\t' 
                    + repr(CP) + u'\t' 
                    + repr(Ent) + u'\t' 
                    + repr(RevEnt) + u'\t' 
                    + repr(Mult) + u'\n')
            else:
                outfile.write(repr(i) + u'\t100\t100\t100\t100\n')

if __name__ == "__main__":

    args = parse_args()
    
    try:
        args.frm
    except NameError:
        args.frm = "NeuralMonkey"
    if args.frm == None:
        args.frm = "NeuralMonkey"
     
    try:
        if args.frm == "NeuralMonkey":
            check_argument("-s (source)",args.src, "NeuralMonkey")
            check_argument("-t (target)",args.trg, "NeuralMonkey")
    except IOError as e:
        sys.exit(e)

    main(args)
    

        