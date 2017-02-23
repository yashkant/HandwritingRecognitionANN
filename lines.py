import cv2 
import numpy as np 
import math

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

thresh2=thresh.copy()
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#Whichever element of contoeur is to be drawn set the 2nd param accordingly on an index of zero, -1 to show all the contours 
#Last arguement draws the boundary in pixels pass -1 for a filled image.
cv2.imshow('Resized',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

for i in range(0,len(contours)-1) :
	area = cv2.contourArea(contours[i])
	cv2.drawContours(im,contours,i,(0,255,0),2)
	cv2.imshow('image1',im)
	# cv2.imshow('image3',thresh2)
	# #cv2.drawContours(im, contours, -1, (0,255,0), 3) #draw all contours
	# contnumber=4
	# cv2.drawContours(im, contours, contnumber, (0,255,0), 3) #draw only contour contnumber
	# cv2.imshow('contours', im)
	# [vx,vy,x,y] = cv2.fitLine(contours[contnumber], cv2.DIST_L2,0,0.01,0.01)
	# lefty = int((-x*vy/vx) + y)
	# righty = int(((cols-x)*vy/vx)+y)
	# cv2.line(im,(cols-1,righty),(0,lefty),(0,255,255),2)
	print "Area = " + str(area)+"    " + str(i)
	# cv2.imshow('result', im)
	# raw_input("Press Enter to terminate.")
	cv2.waitKey(0)
	cv2.destroyAllWindows()

area = cv2.contourArea(contours[i])
cv2.drawContours(im,contours,7,(0,255,0),2)
cv2.imshow('image1',im)
# cv2.imshow('image3',thresh2)
# #cv2.drawContours(im, contours, -1, (0,255,0), 3) #draw all contours
# contnumber=4
# cv2.drawContours(im, contours, contnumber, (0,255,0), 3) #draw only contour contnumber
# cv2.imshow('contours', im)
# [vx,vy,x,y] = cv2.fitLine(contours[contnumber], cv2.DIST_L2,0,0.01,0.01)
# lefty = int((-x*vy/vx) + y)
# righty = int(((cols-x)*vy/vx)+y)
# cv2.line(im,(cols-1,righty),(0,lefty),(0,255,255),2)
print "Area = " + str(area)+"    " + str(i)
# cv2.imshow('result', im)
# raw_input("Press Enter to terminate.")
cv2.waitKey(0)
cv2.destroyAllWindows()



# #Enumerate creates a tuple of indices and the elements of countours.
# for h,cnt in enumerate(contours):
# 	mask = np.zeros(imgray.shape,np.uint8)	
# 	cv2.drawContours(mask,[cnt],0,255,-1)
# 	mean = cv2.mean(im,mask = mask)
