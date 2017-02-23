import cv2 
import numpy as np 
import Neural_Networks as nn 
import Load_MNIST as lm 




img = cv2.imread('3a.jpg')
#cv2.imshow('Image',img)
rimg = cv2.resize(img, (100,100))
rimg = cv2.GaussianBlur(rimg,(5,5),0)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

cv2.imshow('Dip', rimg)
cv2.imshow('Dip1', edges)

cv2.waitKey(0)
cv2.destroyAllWindows()

rimg = cv2.cvtColor( rimg, cv2.COLOR_RGB2GRAY )
# rimg = cv2.GaussianBlur(rimg,(100,100),0)
ret,rimg = cv2.threshold(rimg,127,255,cv2.THRESH_BINARY)
dip = 255 - rimg 
#print rimg 
# dip = cv2.erode(dip,kernel,iterations = 1)
# dip = cv2.dip(img,kernel,iterations = 1)

# print type(binarize)

#This converts the integer values to those of float32 as required in MNIST dataset 
dip = dip.astype(np.float32, copy=False)
dip = dip/255


dip = np.reshape(dip,(10000,1))

for a in dip :
	if(a[0] < 0.43):
		a[0] = 0
	if(a[0] > 0.5):
		a[0] = 1

dip = np.reshape(dip,(100,100))





dip = np.reshape(dip,(784,1))

#print dip
#dip is finally ready to be tested using the network 
train_data , validate_date , test_data = lm.prepare_dataset()
#print test_data[0][0]
net = nn.Network([784,30,20,10])
net.load()
print net.feedforward(dip)
print np.argmax(net.feedforward(dip))
# net.stochastic_gradient_descent(train_data,3,10,3.0,test_data)
# net.save()



# print '{0} -> {1}'.format(np.argmax(net.feedforward(dip)), 2)

#Images captured with devices would also require contrast adjustments since binarizing has not been a good alternative 

