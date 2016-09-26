#!/usr/bin/python
usage = "whiten.py data.pkl"
description = "whitens data and writes into a new output file (name based on the old one)"
author = "reed.essick@ligo.org"

#-------------------------------------------------

### custom packages
import parseData
import whitenData

### standard packages
from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-t', '--time', default=False, action='store_true')

parser.add_option('-m', '--method', default='zeroMean', type='string', help='"zeroMean" or "minMax"')
parser.add_option('-e', '--skip', default=[], action='append', type='string', help='do NOT whiten these cols')

opts, args = parser.parse_args()

assert len(args)==1, 'please supply exactly 1 input argument\n%s'%usage
pklNAME = args[0]

#-------------------------------------------------

### read data
h, d, kwargs = parseData.load_data( pklNAME, verbose=opts.verbose, timing=opts.time )

### whiten data
if opts.method == "zeroMean":
    d = whitenData.zeroMean_whiten( h, d, skip=opts.skip )
elif opts.method == "minMax":
    d = whitenData.minMax_whiten( h, d, skip=opts.skip )
else:
    raise ValueError('--method=%s not understood'%opts.method)

### write data
pklOUT = pklNAME[:-4]+"_%s.pkl"%(opts.method)
parseData.write_data( h, d, pklOUT, verbose=opts.verbose, timing=opts.time, whiten=True, **kwargs)
