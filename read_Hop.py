import cPickle
import gzip
import numpy as np
import os 
import cv2 

def helper(x):
	return{
		'0': 0,
		'1': 1,
		'2': 2,
		'3': 3,
		'4': 4,
		'5': 5,
		'6': 6,
		'7': 7,
		'8': 8,
		'9': 9,
		'a': 10,
		'b': 11,
		'c': 12,
		'd': 13,
		'e': 14,
		'f': 15,
	}[x]


path = os.path.join(os.getcwd(),'Hopkins_MN/data0.dat')
f = open(path,'r')

for i in range(1,100):
	img = np.array([])
	for i in range(1, 784 + 1):
		n = (helper(f.read(1))*16 + helper(f.read(1)))
		img = np.append(img,n)

		if i%2 == 0:
			x = f.read(1)
	img = img/255
	img = np.resize(img, (28,28))
	cv2.imshow('Test',img) 
	cv2.waitKey(0)
	cv2.destroyAllWindows()

