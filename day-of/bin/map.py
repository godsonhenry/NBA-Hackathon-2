#!/usr/bin/python
usage       = "map.py [--options] shotData.pkl playerData.pkl outData.pkl"
description = "reads in shotData.pkl and playerData.pkl, mapping player data into shotData as necessary. Writes the resulting vectorized data into outData.pkl"
author      = "reed.essick@ligo.org"

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

#-----------

assert len(args)==3, 'please supply exactly 3 input arguments\n%s'%usage
pklSHOT, pklPLYR, pklOUT = args

#-------------------------------------------------

### read player data
hplyr, dplyr, kwplyr = parseData.load_data( pklPLYR, verbose=opts.verbose, timing=opts.time )

### read in shot data
hshot, dshot, kwshot = parseData.load_data( pklSHOT, verbose=opts.verbose, timing=opts.time )

#-------------------------------------------------

### stich together data!
h, d = parseData.map_data( hplyr, dplyr, hshot, dshot, verbose=opts.verbose, timing=opts.time )

### map keyword arguments together!
kwargs = dict()
kwargs.update( kwplyr )
kwargs.update( kwshot )

#-------------------------------------------------

### write output
parseData.write_data( h, d, pklOUT, verbose=opts.verbose, timing=opts.time, **kwargs )
