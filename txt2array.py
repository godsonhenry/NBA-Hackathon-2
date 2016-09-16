import numpy as np
import pickle

##############################################
if __name__=='__main__':

	#First parse options
	from optparse import OptionParser

	parser = OptionParser()
	
	parser.add_option("", "--text-file", default=None, type="string", help="Path to textfile containing the data")
	parser.add_option("", "--outdir", default=None, type="string", help="Directory in which to save pickled dictionary")

	opts, args = parser.parse_args()
	
	text_file = opts.text_file
	outdir = opts.outdir
	
	#--------------------------------------------------------------
	
	#Load in data
	array = np.genfromtxt(text_file)
	
	#Load in header
	text_openfile = open(text_file,'rt')
	text_list = text_openfile.readlines()
	headers = np.array(text_list[0].split()[1:])
	text_openfile.close()
	
	#Build dictionary
	dic = {}
	dic['headers'] = headers
	dic['data'] = array
	
	#Pickle the dictionary
	pickle.dump(dic,open('%s/pickled_data_dictionary.pkl'%outdir,'wt'))
	
	
