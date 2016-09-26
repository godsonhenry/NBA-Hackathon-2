#!/usr/bin/python
usage       = "makeFake_playerData.py [--options] out.pkl"
description = "generates fake data in the correct format for classify.py. Assume 2 classes with 2 features, centered at (0,0) and (1,1). Both have the same standard deviation and diagonal covariance matricies"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

import numpy as np

import parseData

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

### verbosity
parser.add_option('-v', '--verbose', default=False, action='store_true')

### distrib paramters
parser.add_option('-s', '--scale', default=0.1, type='float', help='standard deviation')

parser.add_option('-a', '--num-aSamp', default=100, type='int', help='number of samples around 0,0')
parser.add_option('-b', '--num-bSamp', default=100, type='int', help='number of samples around 1,1')

opts, args = parser.parse_args()

#-----------

assert len(args)==1, 'please supply exactly 1 input argument\n%s'%usage
pklOUT = args[0]

#-------------------------------------------------

if opts.verbose:
    print "generating samples about (0,0)"
aSamp = np.random.normal(loc=0, scale=opts.scale, size=(opts.num_aSamp,2))

if opts.verbose:
    print "generating samples about (1,1)"
bSamp = np.random.normal(loc=1, scale=opts.scale, size=(opts.num_bSamp,2))

if opts.verbose:
    print "concatenating"
samp = np.concatenate((aSamp, bSamp))

#-------------------------------------------------

h = np.array(['a', 'b'])
parseData.write_data( h, samp, pklOUT, verbose=opts.verbose )
