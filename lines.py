import cv2 
import numpy as np 
import math
import scipy.misc
import os

#This function extracts the opposite points of a rectangle.
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

#This function arranges the images in order from left to right and also gets the diagonal points 
def arrange(rects):
	ar = [[[1001]]]
	for r in rects:
		tr = getp(r)
		print tr
		for i in range(0, len(ar)):
			if(tr[0][0] < ar[i][0][0]):
				ar.insert(i,tr)
				break
	return ar[:-1]

def saveimages(crops):
	for i in range(1,len(crops)+1) :
		scipy.misc.imsave('outputs/images/outfile'+str(i)+'.jpg', crops[i-1])

def savedata(crops):
	cwd = os.getcwd()
	os.chdir( cwd + '/outputs/data')
	for i in range(0,len(crops)):
		crops[i].dump("data" + str(i+1) +".data")
	os.chdir(cwd)

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
			

im = cv2.imread('nnsample_box.png')
#Saves the dimens of image, I wish to resize the image proportional to its original dimensions.
#The scaling factor is such that width will be 1000 else lesser for low pixel image.

height,width = im.shape[:2]

rwidth = 1000
sfactor = float(width)/rwidth
rheight = int(math.ceil(float(height)/sfactor ))
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
ki = int(math.ceil(float(width)/100))
kernel = np.ones((4,4), np.uint8)
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
	epsilon = 0.025*cv2.arcLength (contours[i],True)
	print epsilon
	approx.append(cv2.approxPolyDP(contours[i],epsilon,True))


#Separate the ones which are rectangles and get their opposite boundary points. :)
rects = []
for i in range(0,len(approx)):
	if(len(approx[i]) == 4):
		rects.append(approx[i])






#Filter unnecessary rectangles if detected.
if(len(rects) > 6):
	rects = filter(rects)


#Arrange in ascending order of x and put in opposite points 
frects = arrange(rects)

#Now cropping the required images from the given points 
crops = []
for r in frects:
	crops.append( im[ r[1][0]:r[1][1], r[0][0]:r[0][1] ] )

saveimages(crops)





# cv2.imshow('Resized',im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# imc = im.copy()
# for i in range(0,len(rects)) :
# 	area = cv2.contourArea(rects[i])
# 	cv2.drawContours(im,rects,i,(0,255,0),2)
# 	cv2.imshow('filtered',im)
# 	print "Area = " + str(area)+"    " +str(len(contours[i])) + "    " +str(i)
# 	print "Area = " + str(area)+"    " +str(len(approx[i])) + "    " +str(i)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()


# for i in range(0,len(rects)) :
# 	area = cv2.contourArea(rects[i])
# 	cv2.drawContours(im,rects,i,(((i%2)+1)*255,(i%2)*255,0),2)
# 	cv2.imshow('before',im)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()





# 	cv2.drawContours(imc,approx,i,(0,255,0),2)
# 	cv2.imshow('after',imc)
# 	print "Area = " + str(area)+"    " +str(len(contours[i])) + "    " +str(i)
# 	print "Area = " + str(area)+"    " +str(len(approx[i])) + "    " +str(i)
# 	# cv2.imshow('result', im)
# 	# raw_input("Press Enter to terminate.")
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()