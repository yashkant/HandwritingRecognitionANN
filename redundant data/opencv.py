import cv2 
import numpy as np 
import Neural_Networks as nn 
import Load_MNIST as lm 

def predictImage(number):
	#This will check results to each separated image.
	img = cv2.imread('outputs/images/outfile'+str(number)+'.jpg')
	rimg = cv2.resize(img, (28,28))
	rimg = cv2.GaussianBlur(rimg,(5,5),0)
	rimg = cv2.cvtColor( rimg, cv2.COLOR_RGB2GRAY )
	# ret,rimg = cv2.threshold(rimg,127,255,cv2.THRESH_BINARY)
	dip = 255 - rimg 
	# dip = cv2.erode(dip,kernel,iterations = 1)
	# dip = cv2.dip(img,kernel,iterations = 1)
	#This converts the integer values to those of float32 as required in MNIST dataset 
	dip = dip.astype(np.float32, copy=False)
	dip = dip/255
	dip = np.reshape(dip,(784,1))
	#Change this manual or use a better for the bottom values
	#filter according to the dataset.
	for a in dip :
		if(a[0] < 0.43):
			a[0] = 0
		if(a[0] > 0.5):
			a[0] = 1

	dip = np.reshape(dip,(28,28))
	cv2.imshow('Dip', dip)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	dip = np.reshape(dip,(784,1))
	#dip is ready to be tested using the network 
	train_data , validate_date , test_data = lm.prepare_dataset()
	net = nn.Network([784,30,20,10])
	net.load()
	print net.feedforward(dip)
	print np.argmax(net.feedforward(dip))

#50% Accuracy as of now has been acheived.
for i in range (1,7):
	predictImage(i)

# net.stochastic_gradient_descent(train_data,3,10,3.0,test_data)
# net.save()
# print '{0} -> {1}'.format(np.argmax(net.feedforward(dip)), 2)
#Images captured with devices would also require contrast adjustments since binarizing has not been a good alternative 

