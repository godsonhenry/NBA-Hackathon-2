#!/usr/bin/python
usage       = "classify.py [--options] train_playerData.pkl predict_playerData.pkl"
description = "perform unsupervised classification based on player statistics. Writes new pkl file (following the same standards) with new columns representing each player's class. Predictions are written inot a standard filename based off predict_playerData.pkl"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

### custom packages
import parseData

### standard packages
import numpy as np

from sklearn.mixture import GMM
from sklearn.cluster import KMeans

import time

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

plt.rcParams.update( {
                       'font.family' : 'serif',
                     }
                   )
import corner

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

### verbosity
parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-t', '--time', default=False, action='store_true', help='print how long important steps take')

parser.add_option('-p', '--plots', default=False, action='store_true', help='generate corner plots as well as classifications. NOT YET IMPLEMENTED!')

### options common for both methods
parser.add_option('-n', '--numClasses', default=2, type='int', help='the number of classes used')

parser.add_option('-e', '--exclude', default=[], action='append', type='string', help='exclude this variable when performing classification. Include it in the output file, though.')
parser.add_option('-m', '--method', default='GMM', type='string', help='the method of classification. either \"GMM\" or \"KMeans\"')

### options for just GMM
parser.add_option('', '--GMM-covarType', default='full', type='string', help='"spherical", "tied", "diag", "full". Defaults to "full".')

### options for just KMeans
### currently we just use the defaults!

### I/O options
parser.add_option('', '--tag', default='', type='string')
parser.add_option('', '--pklModel', default=False, type='string', help='if supplied, pickles trained model into this filename along with headers')

opts, args = parser.parse_args()

#-----------

assert len(args)==2, 'please supply exactly 2 input arguments\n%s'%usage
pklTRAIN, pklPREDICT = args

if opts.tag:
    opts.tag = "_"+opts.tag

opts.verbose = opts.verbose or opts.time

#-------------------------------------------------

### read in training data and exclude columns
h, d, _ = parseData.load_data( pklTRAIN, verbose=opts.verbose, timing=opts.time )
### exclude columns
hsub, dsub = parseData.excludeCols( h, d, opts.exclude, verbose=opts.verbose, timing=opts.time )

### plot everything!
if opts.plots:
    if opts.verbose:
        print "plotting all data points..."
    fig = corner.corner( dsub, labels=hsub )
    figname = pklTRAIN[:-4]+"_corner.png"
    fig.savfig(figname)
    plt.close(fig) 

#-------------------------------------------------

### build unsupervised classification model
if opts.method == "GMM":
    model = GMM( n_components    = opts.numClasses, 
                 covariance_type = opts.GMM_covarType, 
               ) #random_state=None, thresh=None, tol=0.001, min_covar=0.001, n_iter=100, n_init=1, params='wmc', init_params='wmc', verbose=0)

elif opts.method == "KMeans":
    model = KMeans( n_clusters=opts.numClasses, 
                  ) #init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)

else:
    raise ValueError("--method=%s not understood!"%opts.method)

### fit model
if opts.verbose:
    print "fitting model"
    if opts.time:
        t0 = time.time()
model.fit(dsub)
if opts.time:
    print "    %.6f sec"%(time.time() - t0)

del dsub ### get rid of expensive thing...

if opts.pklModel: ### record trained model
    parseData.write_model( hsub, model, opts.pklModel, verbose=opts.verbose, timing=opts.time )

#-------------------------------------------------

### read in prediciton data
h, d, kwargs = parseData.load_data( pklPREDICT, verbose=opts.verbose, timing=opts.time )

### exclude columns
hpredict, dpredict = parseData.excludeCols( h, d, opts.exclude, verbose=opts.verbose, timing=opts.time )

assert np.all(hpredict==hsub), 'pklTRAIN and pklPREDICT disagree on headers!'
del hsub ### get rid of unecessary thing

#-------------------------------------------------

### predict model
if opts.verbose:
    print "making predictions"
    if opts.time:
        t0 = time.time()
klass = model.predict(dpredict)
if opts.time:
    print "    %.6f sec"%(time.time() - t0)

# add this to the original data vectors!
h = list(h) + ['class']
d = list(np.transpose(d)) + [klass]

if opts.method == "GMM": ### also include the posterior probabilities
    if opts.verbose:
        print "retrieving posterior probabilities"
        if opts.time:
            t0 = time.time()
    probs = model.predict_proba(dpredict)
    if opts.time:
        print "    %.6f sec"%(time.time() - t0)

    # add this to the original data vectors!
    h = list(h) + ['prob(%d)'%i for i in xrange(opts.numClasses)]
    d = d + list(np.transpose(probs))

h = np.array(h)
d = np.transpose(np.array(d))

if opts.verbose:
    print "writing %d columns"%len(h)
    print "writing %d rows"%len(d)

#-------------------------------------------------

### write output file
pklOUT = pklPREDICT[:-4]+"_%s%s.pkl"%(opts.method, opts.tag)
parseData.write_data( h, d, pklOUT, verbose=opts.verbose, timing=opts.time, classifyExclude=opts.exclude, **kwargs)

### plot each class!
if opts.plots:
    for klass in xrange(opts.numClasses):
        if opts.verbose:
            print "plotting data points for class : %d"%(klass)
        truth = d[:,h=='class'] == klass
        fig = corner.corner( dsub[truth,:], labels=hsub )
        figname = pklTRAIN[:-4]+"_corner-%d.png"%klass
        fig.savfig(figname)
        plt.close(fig)
