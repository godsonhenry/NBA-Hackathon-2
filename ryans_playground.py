import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor

#-----------------------------------------------------------------------

####################
### Load in data ###
####################

#Load in data
dic = pickle.load(open('pickled_data_dictionary.pkl'))
data = dic['data']
headers = dic['headers']

#Separate out X and y
X = data[:,headers != 'BSN']
y = data[:,headers == 'BSN'].reshape(-1)

#Normalize all X parameters
X_norm = np.ones(X.shape)*np.nan
for i in xrange(len(X[0])):
	X_norm[:,i] = (X[:,i]-np.min(X[:,i])) / np.max(X[:,i]-np.min(X[:,i]))
	
#print X
#print X_norm

#-----------------------------------------------------------------------

######################
### Random Forests ###
######################

#Initialize index at which we want to split training and cross-validation data sets
i_divide = 6000

#Initialize random forest object (runtime appears to increase linearly with number of estimators and decrease linearly with number of jobs)
rf = RandomForestRegressor(n_estimators=500,max_features=None,max_depth=None,min_samples_split=1,oob_score=True, n_jobs=4)
rf_norm = RandomForestRegressor(n_estimators=500,max_features=None,max_depth=None,min_samples_split=1,oob_score=True, n_jobs=4)
rf_extra = ExtraTreesRegressor(n_estimators=500,max_features=None,max_depth=None,min_samples_split=1,oob_score=True, n_jobs=4, bootstrap=True)

#Fit the data
rf.fit(X[:i_divide],y[:i_divide])
rf_norm.fit(X_norm[:i_divide],y[:i_divide])
rf_extra.fit(X_norm[:i_divide],y[:i_divide])

#Print score and OOB score
print "Raw ", rf.score(X[i_divide:],y[i_divide:])
print "Raw", rf.oob_score_

print "Normed ", rf_norm.score(X_norm[i_divide:],y[i_divide:])
print "Normed ", rf_norm.oob_score_

print "Extra ", rf_extra.score(X_norm[i_divide:],y[i_divide:])
print "Extra ", rf_extra.oob_score_

#Print parameter importances
print "Raw ", rf.feature_importances_
print "Normed ", rf_norm.feature_importances_
print "Extra ", rf_extra.feature_importances_

