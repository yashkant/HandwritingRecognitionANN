
# coding: utf-8

# In[51]:

import os
import cv2 
import numpy as np 
os.chdir('/home/mehak/Desktop/Neural Networks/Handwriting Recognition/')
import Neural_Networks as nn 
import Load_MNIST as lm
import math
import scipy.misc
import sys


# In[52]:

#This function extracts the opposite points of a rectangle.
def getp(rect):
    x = []; y=[];
    for i in range(0,4):
        x.append(rect[i][0][0])
        y.append(rect[i][0][1])
    x.sort()
    y.sort()
    return[[x[1],x[2]],[y[1],y[2]]]


# In[53]:

def show_image(im):
    cv2.imshow('new',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# In[89]:

#All the images are have dimensions greater than 50x50
def cropi(im):
    try:
        h,w = im.shape[:2]
        roi = im[6:h-10, 10:w-15]
        return roi
    except:
        return im
        


# In[55]:

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


# In[56]:

def saveimages(crops):
    for i in range(1,len(crops)+1) :
        print i
        scipy.misc.imsave('outfile'+str(i)+'.jpg', crops[i-1])
        


# In[57]:

def savedata(crops):
    os.chdir( cwd + '/outputs/data')
    for i in range(0,len(crops)):
        crops[i].dump("data" + str(i+1) +".data")
    os.chdir(cwd)


# In[58]:

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


# In[59]:

#Setting to 650 by default change as required, lower than this won't be scaled.
def initialize_image(file_name):
    im = cv2.imread(file_name)
    height,width = im.shape[:2]
    # im = im[int(height*.25): int(height*0.75), int(width*.25):int(width*.75)]
    print height;print width
    rwidth = 400
    sfactor = float(width)/rwidth
    rheight = int(math.ceil(float(height)/sfactor ))
    if(sfactor > 1):
        return cv2.resize(im, (rwidth,rheight))
    else:
        return im


# In[60]:

def show_contours(rects):
    for i in range(0,len(rects)) :
        area = cv2.contourArea(rects[i])
        cv2.drawContours(im,rects,i,(((i%2)+1)*255,(i%2)*255,0),2)
        cv2.imshow('before',im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# In[61]:

#Reading all files from the folder and returning a list 
# get_list(1)

def get_list(dir_no):
    os.chdir('/home/yash/Desktop/Neural Networks/Handwriting Recognition/dataset/' )
    list = os.listdir(str(dir_no))
    return list


# In[62]:

def vectorize(i):
    a= np.zeros(10)
    a[i] = 1
    a = np.reshape(a,(10,1))
    return a


# In[63]:

def make_train_set():
    training_set = []
    for dir_no in range (0,10):
        lis = get_list(dir_no)
        t_data = process(dir_no, lis)
        training_set += t_data
        print len(lis)
    return training_set


# In[64]:

#Process Images from a particular folder.
#assuming present path to be at Handwriting Recoginition
def process(dir_no, im_list):
    os.chdir('/home/yash/Desktop/Neural Networks/Handwriting Recognition/dataset/' + str(dir_no) + '/')
    print os.getcwd()
    x = []
    for im in im_list:
        img = cv2.imread(im)
        height,width = img.shape[:2]
        rimg = cv2.resize(img, (28,28))
        ret,rimg = cv2.threshold(rimg,127,255,cv2.THRESH_BINARY)
        rimg = cv2.GaussianBlur(rimg,(1,1),0) 
        rimg = cv2.cvtColor( rimg, cv2.COLOR_RGB2GRAY )
        dip = 255 - rimg
        dip = cv2.dilate(dip, np.ones((2,2)))
        dip = dip.astype(np.float32, copy=False)
        dip = dip/255
        dip = np.reshape(dip, (784,1))
        x.append((dip,vectorize(dir_no)))
    return x


# In[66]:

#Saves the dimens of image, I wish to resize the image proportional to its original dimensions.
#The scaling factor is such that width will be 1000 else lesser for low pixel image.
file_name = sys.argv[1]
im = initialize_image(file_name)
height,width = im.shape[:2]
print height 
print width


# In[67]:

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.fastNlMeansDenoising(imgray,None,10,7,21)
#Thresholding requires a grayscale image 2nd param : threshvalue and 3rd param : maxValue of a pixel
thresh = cv2.Canny(imgray, 60, 200)
#Closing is dialation followed by erosion helps to fill out the gaps left out by creases in paper or disconnected components.
#Size of kernel is area of sliding window, I think it should be proportional to the size of image/boxes we will be using.
ki = int(math.ceil(float(width)/100))
kernel = np.ones((ki,ki), np.uint8)
print ki
# kernel = np.ones((4,4), np.uint8)
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
    approx.append(cv2.approxPolyDP(contours[i],epsilon,True))

#Separate the ones which are rectangles. :)
rects = []
for i in range(0,len(approx)):
    if(len(approx[i]) == 4):
        rects.append(approx[i])

        
if(len(rects) > 6):
    rects = filter(rects)
im = initialize_image(file_name)
#Arrange in ascending order of x and put in opposite points 
frects = arrange(rects)
#Ahead of this show_contours won't work as only opposite points are returned.
im = initialize_image(file_name)
crops = []
for r in frects:
    crops.append( im[ r[1][0]:r[1][1], r[0][0]:r[0][1] ] )
# saveimages(crops)


# In[68]:

show_contours(rects) 


# In[111]:

train_set = make_train_set()
net = nn.Network([784,30,10])
os.chdir('/home/yash/Desktop/Neural Networks/Handwriting Recognition/')
net.load()


# In[114]:

# np.shape(mnist.test.images)  Gives (10000, 784) 
# np.shape(mnist.test.labels) Gives (10000, 10)
# print(sess.run(tf.argmax(y,1), feed_dict={x: mnist.test.images})) Gives [7 2 1 ..., 4 8 6]
"""Give a proper Thresholding now."""
os.chdir('/home/yash/Desktop/Neural Networks/Handwriting Recognition/')
def predict():
    x = []
    for crop in crops:
        crop = cropi(crop)
        rimg = cv2.resize(crop, (28,28))
        ret,rimg = cv2.threshold(rimg,127,255,cv2.THRESH_BINARY)
        rimg = cv2.GaussianBlur(rimg,(1,1),0) 
        rimg = cv2.cvtColor( rimg, cv2.COLOR_RGB2GRAY )
        dip = 255 - rimg
        dip = cv2.dilate(dip, np.ones((1,1)))
        dip = dip.astype(np.float32, copy=False)
        dip = dip/255
        show_image(dip)
        dip = np.reshape(dip, (784,1))
        a=np.argmax(net.feedforward(dip))
        print a
        x.append(a)
    return x


# In[115]:

pin = predict()
print ''.join(str(x) for x in pin)


# In[ ]:



