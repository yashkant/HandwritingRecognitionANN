import numpy as np
import cv2
import xlsxwriter

image = cv2.imread('cow.png')
gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5) ,0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(thresh,kernel,iterations = 1)
thresh = cv2.dilate(erosion,kernel,iterations = 1)
cv2.imshow('thresh',thresh)
_,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

array = np.zeros((1,100))

for cnt in contours:
    if cv2.contourArea(cnt)>100:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  h>30:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            x = roismall.reshape((1,100))
            array = np.append(array,x,axis = 0)

            cv2.imshow('trial',roismall)
            cv2.imshow('image',image)
            cv2.waitKey(0)
#cv2.destroyAllWindows(0)
print(array[2].reshape((10,10)))


workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet = workbook.add_worksheet()


row = 0

for col, data in enumerate(array[3]):
    worksheet.write_column(row, col, data)

workbook.close()
