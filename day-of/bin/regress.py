#!/usr/bin/python
usage       = "regress.py [--options] costFooKey train_data.pkl predict_data.pkl" 
description = "regress cost function from the data provided"
author      = "reed.essick@ligo.org"

#-------------------------------------------------

### custom packages
import parseData

### standard packages
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor

from sklearn.svm import SVR
from sklearn.svm import NuSVR

import time

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

plt.rcParams.update( {
                       'font.family' : 'serif',
                     }
                   )

from optparse import OptionParser

#-------------------------------------------------

parser = OptionParser(usage=usage, description=description)

### verbosity
parser.add_option('-v', '--verbose', default=False, action='store_true')
parser.add_option('-V', '--Verbose', default=False, action='store_true')
parser.add_option('-t', '--time', default=False, action='store_true', help='print how long important steps take')

parser.add_option('-p', '--plots', default=False, action='store_true', help='generate corner plots. NOT YET IMPLEMENTED!')

### options common to all methods
parser.add_option('-e', '--exclude', default=[], action='append', type='string', help='exclude this variable when performing classification. Include it in the output file, though.')
parser.add_option('-m', '--method', default='RandomForest', type='string', help='"RandomForest", "ExtraTrees", "AdaBoost", "SVR", or "NuSVR"')

### options for all Forests
parser.add_option('', '--n-estimators', default=10, type='int')

### options for RandomForest and ExtraTrees
#RandomForestRegressor(n_estimators=10, criterion='mse', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False)
#ExtraTreesRegressor(n_estimators=10, criterion='mse', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, bootstrap=False, oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False)
parser.add_option('', '--n-jobs', default=-1, type='int')

### options for AdaBoost
#AdaBoostRegressor(base_estimator=None, n_estimators=50, learning_rate=1.0, loss='linear', random_state=None)

### options for SVR
#SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)

### options for NuSVR
#NuSVR(nu=0.5, C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, tol=0.001, cache_size=200, verbose=False, max_iter=-1)

### I/O options
parser.add_option('', '--tag', default='', type='string')
parser.add_option('', '--pklModel', default=False, type='string', help='if supplied, pickles trained model into this filename along with headers')

opts, args = parser.parse_args()

#-----------

assert len(args)==3, 'please supply exactly 3 input arguments\n%s'%usage
costFooKey, pklTRAIN, pklPREDICT = args

opts.exclude.append(costFooKey) ### always exclude costFooKey!

opts.verbose = opts.verbose or opts.Verbose or opts.time

if opts.tag:
    opts.tag = "_"+opts.tag

#-------------------------------------------------

### read in training data
h, d, kw = parseData.load_data( pklTRAIN, verbose=opts.verbose, timing=opts.time )

### extract cost function data
if opts.verbose:
    print "extracting costFooKey=%s"%costFooKey
assert np.sum(h==costFooKey)==1, 'could not find a unique column matching costFooKey=%s'%costFooKey
costFoo = d[:,h==costFooKey].ravel()

### exclude variables
hsub, dsub = parseData.excludeCols( h, d, opts.exclude, verbose=opts.verbose, timing=opts.time )

#-------------------------------------------------

### build supervised classification model

if opts.method == "RandomForest":
    model = RandomForestRegressor( 
                                   verbose                  = opts.Verbose,
                                   n_estimators             = opts.n_estimators, 
                                   n_jobs                   = opts.n_jobs, 
                                   bootstrap                = True, 
#                                   criterion                = 'mse', 
#                                   max_depth                = None, 
#                                   min_samples_split        = 2, 
#                                   min_samples_leaf         = 1, 
#                                   min_weight_fraction_leaf = 0.0, 
#                                   max_features             = 'auto', 
#                                   max_leaf_nodes           = None, 
#                                   oob_score                = False, 
#                                   warm_start               = False
                                 )

elif opts.method == "ExtraTrees":
    model = ExtraTreesRegressor( 
                                 verbose                  = opts.Verbose,
                                 n_estimators             = opts.n_estimators, 
                                 n_jobs                   = opts.n_jobs, 
                                 bootstrap                = True, 
#                                 criterion                = 'mse', 
#                                 max_depth                = None, 
#                                 min_samples_split        = 2, 
#                                 min_samples_leaf         = 1, 
#                                 min_weight_fraction_leaf = 0.0, 
#                                 max_features             = 'auto', 
#                                 max_leaf_nodes           = None, 
#                                 oob_score                = False, 
#                                 warm_start               = False,
                               )

elif opts.method == "AdaBoost":
    model = AdaBoostRegressor( 
                               n_estimators = opts.n_estimators,
#                               base_estimator=None, 
#                               learning_rate=1.0, 
#                               loss='linear', 
#                               random_state=None
                              )

elif opts.method == "SVR":
    model = SVR( 
                 verbose    = False,  
#                 kernel     = 'rbf', 
#                 degree     = 3, 
#                 gamma      = 'auto', 
#                 coef0      = 0.0, 
#                 tol        = 0.001, 
#                 C          = 1.0, 
#                 epsilon    = 0.1, 
#                 shrinking  = True, 
#                 cache_size = 200, 
#                 max_iter   = -1,
               )

elif opts.method == "NuSVR":
    model = NuSVR( 
                   verbose    = opts.Verbose, 
#                   nu         = 0.5, 
#                   C          = 1.0, 
#                   kernel     = 'rbf', 
#                   degree     = 3, 
#                   gamma      = 'auto', 
#                   coef0      = 0.0, 
#                   shrinking  = True, 
#                   tol        = 0.001, 
#                   cache_size = 200, 
#                   max_iter   = -1,
                 )

else:
    raise ValueError('--method=%s not understood!'%opts.method)

### fit model
if opts.verbose:
    print "fitting model"
    if opts.time:
        t0 = time.time()
model.fit( dsub, costFoo )
if opts.time:
    print "    %.6f sec"%(time.time() - t0)

del dsub ### get rid of expensive thing

if opts.pklModel: ### record trained model
    parseData.write_model( hsub, model, opts.pklModel, verbose=opts.verbose, timing=opts.time )

#-------------------------------------------------

### load in prediction data
h, d, kwargs = parseData.load_data( pklPREDICT, verbose=opts.verbose, timing=opts.time )

### cost function for prediction data
if opts.verbose:
    print "extracting costFooKey=%s"%costFooKey
assert np.sum(h==costFooKey)==1, 'could not find a unique column matching costFooKey=%s'%costFooKey
cFpredict = d[:,h==costFooKey].ravel()

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
prediction = model.predict(dpredict)
if opts.time:
    print "    %.6f sec"%(time.time() - t0)

#------- MAIN ANSWERS ------------------

score = model.score(dpredict, cFpredict)
print "score : %.6f"%(score)
print "MSE   : %.6f"%(1-score)
print "important features :"
importance = zip(hpredict, model.feature_importances_)
importance.sort(key=lambda l: l[1], reverse=True)
for key, importance in importance:
    print "    %.6f    : %s"%(importance, key)

if opts.plots:
    ### histogram of feature importance
    fig = plt.figure()
    ax  = fig.gca()

    ncol = np.shape(dpredict)[1]

#    ax.hist( np.log(model.feature_importances_), bins=ncol/5, weights=np.ones((ncol,),dtype=float)/ncol )
    ax.hist( model.feature_importances_, bins=ncol/5, weights=np.ones((ncol,),dtype=float)/ncol )

    ax.set_title('Histogram of Feature Importance')
    ax.set_xlabel('\"importance\"')
    ax.set_ylabel('fraction of features')

    figname = 'regress%s.png'%opts.tag
    if opts.verbose:
        print "        "+figname
    fig.savefig(figname)
    plt.close(fig)

#---------------------------------------

# add this to the original data vectors!
h = np.array(list(h) + ['prediction'])
d = np.transpose(np.array(list(np.transpose(d)) + [prediction]))

if opts.verbose:
    print "writing %d columns"%len(h)
    print "writing %d rows"%len(d)

#-------------------------------------------------

### write output file
pklOUT = pklPREDICT[:-4]+"_%s%s.pkl"%(opts.method, opts.tag)
parseData.write_data( h, d, pklOUT, verbose=opts.verbose, timing=opts.time, costFooKey=costFooKey, regressExclude=opts.exclude, **kwargs)
