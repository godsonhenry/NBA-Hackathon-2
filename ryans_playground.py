import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.mixture import GMM

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
"""
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
print headers[headers != 'BSN']
print "Raw ", rf.feature_importances_
print "Normed ", rf_norm.feature_importances_
print "Extra ", rf_extra.feature_importances_
"""

#-----------------------------------------------------------------------

###############################
### Gaussian Mixture Models ###
###############################

#Initialize index at which we want to split training and cross-validation data sets
i_divide = 10000

#Initialize GMM object
gmm_2 = GMM(n_components=2, covariance_type='full')
gmm_3 = GMM(n_components=4, covariance_type='full')

#Fit the data
gmm_2.fit(X_norm[:i_divide])
gmm_3.fit(X_norm[:i_divide])

#Print means of the fit
print headers[headers != 'BSN']
print "2 models ", gmm_2.means_
print "3 models ", gmm_3.means_

#Print BIC and score
print "2 models ", gmm_2.bic(X_norm[i_divide:])
print "3 models ", gmm_3.bic(X_norm[i_divide:])

#Print probability under each Gaussian model
print "2 models ", gmm_2.predict_proba(X_norm[i_divide:])
print "3 models ", gmm_3.predict_proba(X_norm[i_divide:])

#Print classifications
print "2 models ", gmm_2.predict(X_norm[i_divide:])
print "3 models ", gmm_3.predict(X_norm[i_divide:])


