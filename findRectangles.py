import cv2 
import numpy as np 

img = cv2.imread('test.jpg')
img = cv2.resize(img, (1000,1000))
img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
blur = cv2.GaussianBlur(img,(5,5),0)

#Better results are obtained after blurring and then threholding.
#TODO : try with the images as well.

th2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
minThreshold = 50
maxThreshold = 100
edges = cv2.Canny(th2,minThreshold,maxThreshold,apertureSize = 3)
minLineLength = 100
maxLineGap = 10


lines = cv2.HoughLinesP(edges,1,np.pi/180,20, minLineLength, maxLineGap)
print len(lines)

for k in lines:
	for x1,y1,x2,y2 in k:
		cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)



cv2.imshow('Dip', edges)
cv2.imshow('Dip1', img)
cv2.imshow('Dip2', th2)
cv2.waitKey(0)
cv2.destroyAllWindows()



