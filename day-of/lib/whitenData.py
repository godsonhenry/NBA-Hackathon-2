description = "module that standardizes whitening"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

### standard packages
import numpy as np

#-------------------------------------------------

def get_col( h, skip ):
    return [ i for i in xrange(len(h)) if (h[i] not in skip)]

def zeroMean_whiten( h, d, skip=[] ):
    """
    returns data that is zero-mean and normalized to have std=1
    """
    for icol in get_col( h, skip ):
        d[:,icol] -= np.mean(d[:,icol])
        d[:,icol] /= np.std(d[:,icol])

    return d

def minMax_whiten( h, d, skip=[] ):
    """
    map data to range 0, 1
    """
    for icol in get_col( h, skip ):
        d[:, icol] -= np.min(data[:,icol])
        colmax = np.max(data[:,icol])
        if colmax: ### not zero! 
            d[:, icol] /= np.max(data[:,icol]) ### will break if they're all zero!

    return d
