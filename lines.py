import cv2 
import numpy as np 
import math
import scipy.misc
import os

def getp(rect):
	x1 = width; y1 = height ; x2 = 0; y2 = 0
	
	for i in range(0,4):
		if(rect[i][0][0] > x2):
			x2 = rect[i][0][0]
		
		if(rect[i][0][0] < x1):
			x1 = rect[i][0][0]
		
		if(rect[i][0][1] > y2):
			y2 = rect[i][0][1]
		
		if(rect[i][0][1] < y1):
			y1 = rect[i][0][1]
	
	return [[x1,x2],[y1,y2]]


def saveimages(crops):
	for i in range(1,len(crops)+1) :
		scipy.misc.imsave('outputs/images/outfile'+str(i)+'.jpg', crops[i-1])

def savedata(crops):
	cwd = os.getcwd()
	os.chdir( cwd + '/outputs/data')
	for i in range(0,len(crops)):
		crops[i].dump("data" + str(i+1) +".data")
	os.chdir(cwd)


im = cv2.imread('box.jpg')
#Saves the dimens of image, I wish to resize the image proportional to its original dimensions.
#The scaling factor is such that height will be greater than or equal to 500.
height,width = im.shape[:2]

rheight = 1000
sfactor = float(height)/rheight
rwidth = int(math.ceil(float(width)/sfactor ))
if(sfactor > 1):
	im = cv2.resize(im, (rwidth,rheight))

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.fastNlMeansDenoising(imgray,None,10,7,21)



#Thresholding requires a grayscale image 2nd param : threshvalue and 3rd param : maxValue of a pixel
ret,thresh = cv2.threshold(imgray,125,255,0)
ret,thresh = cv2.threshold(imgray,125,255,0)
thresh = (255-thresh)
#Closing is dialation followed by erosion helps to fill out the gaps left out by creases in paper or disconnected components.
#Size of kernel is area of sliding window, I think it should be proportional to the size of image/boxes we will be using.
kernel = np.ones((30,30), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


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
	epsilon = 0.1*cv2.arcLength (contours[i],True)
	approx.append(cv2.approxPolyDP(contours[i],epsilon,True))

#Separate the ones which are rectangles and get their opposite boundary points. :)
rects = []
for i in range(0,len(approx)):
	if(len(approx[i]) == 4):
		rects.append(getp(approx[i]))

#Now cropping the required images 
crops = []
for r in rects:
	crops.append( im[ r[1][0]:r[1][1], r[0][0]:r[0][1] ] )

saveimages(crops)


cv2.imshow('Resized',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

imc = im.copy()
for i in range(0,len(contours)) :
	area = cv2.contourArea(contours[i])	
	cv2.drawContours(im,contours,i,(0,255,0),2)
	cv2.imshow('before',im)
	cv2.drawContours(imc,approx,i,(0,255,0),2)
	cv2.imshow('after',imc)
	print "Area = " + str(area)+"    " +str(len(contours[i])) + "    " +str(i)
	print "Area = " + str(area)+"    " +str(len(approx[i])) + "    " +str(i)
	cv2.waitKey(0)
	cv2.destroyAllWindows()







# for i in range(0,len(contours)) :
# 	area = cv2.contourArea(contours[i])	
# 	cv2.drawContours(im,contours,i,(0,255,0),2)
# 	cv2.imshow('before',im)
# 	cv2.drawContours(imc,approx,i,(0,255,0),2)
# 	cv2.imshow('after',imc)
# 	print "Area = " + str(area)+"    " +str(len(contours[i])) + "    " +str(i)
# 	print "Area = " + str(area)+"    " +str(len(approx[i])) + "    " +str(i)
# 	# cv2.imshow('result', im)
# 	# raw_input("Press Enter to terminate.")
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()