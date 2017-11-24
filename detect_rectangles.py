
# coding: utf-8

# In[184]:

import cv2 
import numpy as np 
import math
import scipy.misc
import os
from PIL import Image



# In[185]:

#This function extracts the opposite points of a rectangle.
def getp(rect):
    x = []; y=[];
    for i in range(0,4):
        x.append(rect[i][0][0])
        y.append(rect[i][0][1])
    x.sort()
    y.sort()
    return[[x[1],x[2]],[y[1],y[2]]]


# In[186]:

print getp([[[3,5]],[[4,10]],[[10,4]],[[12,13]]])


# In[187]:

#This function arranges the images in order from left to right and also gets the diagonal points 
def arrange(rects):
	ar = [[[1001000]]]
	for r in rects:
		tr = getp(r)
		print tr
		for i in range(0, len(ar)):
			if(tr[0][0] < ar[i][0][0]):
				ar.insert(i,tr)
				break
	return ar[:-1]


# In[197]:

def saveimages(crops):
	for i in range(1,len(crops)+1) :
		scipy.misc.imsave('outputs/images/outfile'+str(i)+'.jpg', crops[i-1])
        


# In[189]:

def savedata(crops):
    os.chdir( cwd + '/outputs/data')
    for i in range(0,len(crops)):
        crops[i].dump("data" + str(i+1) +".data")
    os.chdir(cwd)


# In[190]:

#This function provides us with six nearly equal rectangles 
def filter(rects):
	tps = [[0]]
	for r in rects:
		area = cv2.contourArea(r)
		print area
		x = True
		for tp in tps:
			if(area > 0.8*tp[0] and area < 1.2*tp[0]):
				tp.append(r)
				x = False
		if(x):
			tps.append([area,r])
	for tp in tps:
		if (len(tp) == 7 and tp[0] > 28*28):
			return tp[1:]


# In[191]:


# print os.getcwd() 
# print os.path.realpath(_0_file__)
# file_path os.path.realpath(_0_file__)
# file_name = os.path.basename()
file_path = os.path.realpath(__file__)
dir_path = file_path.rsplit('/',1)
dir_path = dir_path[0]
os.chdir(dir_path)
#Saves the dimens of image, I wish to resize the image proportional to its original dimensions.
#The scaling factor is such that width will be 1000 else lesser for low pixel image.
im = cv2.imread('test.jpg')
height,width = im.shape[:2]
# rwidth = 1000
# sfactor = float(width)/rwidth
# rheight = int(math.ceil(float(height)/sfactor ))
# if(sfactor > 1):
# 	im = cv2.resize(im, (rwidth,rheight))

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.fastNlMeansDenoising(imgray,None,10,7,21)


# In[192]:

#Thresholding requires a grayscale image 2nd param : threshvalue and 3rd param : maxValue of a pixel
ret,thresh = cv2.threshold(imgray,125,255,0)
ret,thresh = cv2.threshold(imgray,125,255,0)
thresh = (255-thresh)
# print os.getcwd()
#Closing is dialation followed by erosion helps to fill out the gaps left out by creases in paper or disconnected components.
#Size of kernel is area of sliding window, I think it should be proportional to the size of image/boxes we will be using.
ki = int(math.ceil(float(width)/100))
# kernel = np.ones((ki,ki), np.uint8)
kernel = np.ones((4,4), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


# In[193]:

#Countours are curves joining all the continuous points having same colour or intensity.
#http://opencvpython.blogspot.in/2012/06/hi-this-article-is-tutorial-which-try.html
#The result "contours" is a Python list, where it contains all objects boundary points as separate lists.
#Whichever element of contoeur is to be drawn set the 2nd param accordingly on an index of zero, -1 to show all the contours 
#Last arguement draws the boundary in pixels pass -1 for a filled image.
thresh2=thresh.copy()
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


#Contour Approximation to detect shapes.
approx = []
for i in range(0,len(contours)) :
	epsilon = 0.025*cv2.arcLength (contours[i],True)
	approx.append(cv2.approxPolyDP(contours[i],epsilon,True))


# In[194]:

#Separate the ones which are rectangles. :)
rects = []
for i in range(0,len(approx)):
	if(len(approx[i]) == 4):
		rects.append(approx[i])

#Filter unnecessary rectangles if detected.
#Change this 6 by the no of integers required to be detected from the image which are placed in boxes.

if(len(rects) > 6):
	rects = filter(rects)


# In[195]:

#Display detected rectangles not arranged on x axis till now.
im = cv2.imread('test.jpg')
for i in range(0,len(rects)) :
	area = cv2.contourArea(rects[i])
	cv2.drawContours(im,rects,i,(((i%2)+1)*255,(i%2)*255,0),2)
	cv2.imshow('before',im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


# In[198]:


#Arrange in ascending order of x and put in opposite points 
frects = arrange(rects)

#Cropping required from the inner sides of the edges.
im = cv2.imread('test.jpg')

crops = []
for r in frects:
    crops.append( im[ r[1][0]:r[1][1], r[0][0]:r[0][1] ] )
for crop in crops:
    cv2.imshow('crops',crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
saveimages(crops)




