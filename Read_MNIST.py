import cv2 
import numpy as np 
import Neural_Networks as nn 
import Load_MNIST as lm 


"""Sample Code to read the MNIST Dataset. """
train_data , validate_date , test_data = lm.prepare_dataset()

for test in test_data:
	aas = test[0].reshape((28,28))
	cv2.imshow('Test',aas) 
	cv2.waitKey(0)
	cv2.destroyAllWindows()
