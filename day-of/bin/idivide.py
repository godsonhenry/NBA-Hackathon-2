#!/usr/bin/python
usage = "idivide.py data.pkl"
description = "divides data set"
author = "reed.essick@ligo.org"

#-------------------------------------------------

### custom packages
import parseData

### default packages
import numpy as np

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-t', '--time', default=False, action='store_true', help='print how long important steps take')

parser.add_option('-f', '--frac', default=0.9, type='int', help='fraction of events written into TRAIN file')

opts, args = parser.parse_args()

#-----------

assert len(args)==1, 'supply 1 input argument\n%s'%usage
pklIN = args[0]

#-------------------------------------------------

### load data
h, d, kwargs = parseData.load_data( pklIN, verbose=opts.verbose, timing=opts.time )

nrow, ncol = np.shape(d)

### find index where we split data
i = max(1, min(nrow-1, nrow*opts.frac))

if opts.verbose:
    print "    idiv : %d"%(i)

### write data
pklOUT = pklIN[:-4]+"_TRAIN.pkl"
parseData.write_data( h, d[:i,:], pklOUT, verbose=opts.verbose, timing=opts.time ) 


pklOUT = pklIN[:-4]+"_PREDICT.pkl"
parseData.write_data( h, d[i:,:], pklOUT, verbose=opts.verbose, timing=opts.time ) 
