#!/usr/bin/python
usage = "bool2cmd.py data.pkl bool.pkl"
description = "reads in a data.pkl file to get headers and a bool.pkl to get a boolean of which we want. Then writes the appropriate command-line option to exclude things we do not want. NOTE: bool=True means we KEEP that header"
author = "reed.essick@ligo.org"

#-------------------------------------------------

### custom packages
import parseData

### standard packages
from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-t', '--time', default=False, action='store_true', help='print how long important steps take')

opts, args = parser.parse_args()

assert len(args)==2, 'please supply exactly 2 input arguments\n%s'%usage
pklDATA, pklBOOL = args

#-------------------------------------------------

### load header data
h, _, _ = parseData.load_data( pklDATA, verbose=opts.verbose, timing=opts.time )

### load bool data
b = parseData.load_bool( pklBOOL, verbose=opts.verbose, timing=opts.time )

### print command line
s = ""
for keep in h[b]:
    s += " -e \"%s\""%keep

print s
