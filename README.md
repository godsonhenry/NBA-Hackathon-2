# NBA-Hackathon

Mostly for training purposes and practice (we're talking about practice?)

Here's the basic plan for the architecture.

We have one script that converts ascii tables to pickled dictionaries (txt2array.py). The dictionaries will have 3 keys:
  - data : a numpy array, with each row containing one entry
  - columns : string descriptions of each column. len(columns) must equal np.shape(data)[1]
  - mask : a boolean array describing which columns we actually want to use

We then have interchangable scripts that each must pick up the pickled dictionary, format the data as needed, and train a machine learning algorithm (provided within scikit-learn) based on the data. These scripts must pickle the *trained* object into a file.

Because all scikit-learn objects will have a "predict" method, we standardize the actual evaluation in a single script (predict.py) that picks up the pickled scikit-learn objects and evaluates the functions at a common set of points for all algorithms. This should be able to take multiple trained objects (ie: multiple files) and evaluate them all at the same points. Then, it should plot or summarize or report the results in some standardized way (eg: overlayed plots).
