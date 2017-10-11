
#Re structuring code for the MNIST Dataset . This script deserializes the dataset and formats it to used in Neural Networks.

import cPickle
import gzip
import numpy as np
import os 


#This function is used to deserialize the dataset from .pkl.gz file 
def load_mnist():

	path = os.path.join(os.getcwd(),'MNIST/mnist.pkl.gz')
	f = gzip.open(path,'rb')
	trainer_data , validator_data , tester_data = cPickle.load(f)
	f.close()
	return (trainer_data , validator_data , tester_data)

#This is the main function that calls load data and also formats it accordingly to be processed by Neural Nets ahead.
def  prepare_dataset():

	trd, vad, tsd = load_mnist()

	trainer_inputs = [np.reshape(x,(784,1)) for x in trd[0]]
	trainer_results = [vectorize(x) for x in trd[1]]
	trainer_data = zip(trainer_inputs, trainer_results)

	validator_inputs = [np.reshape(x , (784,1)) for x in vad[0]]
	validator_data = zip(validator_inputs, vad[1])

	tester_inputs = [np.reshape(x, (784, 1)) for x in tsd[0]]
	tester_data = zip(tester_inputs, tsd[1])

	return trainer_data, validator_data , tester_data


def vectorize(x):

	a = np.zeros((10,1))
	a[x] = 1
	return a


