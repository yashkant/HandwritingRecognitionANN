import cv2
import numpy as np
from keras.datasets import mnist
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend as K
K.set_image_dim_ordering('th')
from resizeimage import resizeimage
from PIL import Image


def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model



seed = 7
image = cv2.imread('/root/Downloads/six.png')
r = 100.0 / image.shape[1]
dim = (100, int(image.shape[0] * r))

# perform the actual resizing of the image and show it
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
image_grey_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#thresholded_image = cv2.adaptiveThreshold(image_grey_scale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
ret_val, thresholded_image = cv2.threshold(image_grey_scale, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#small = cv2.resize(image, (0, 0), fx=fxx, fy=fyy)
resized_image = cv2.resize(thresholded_image, (28, 28))
print(resized_image.shape)
#cv2.imshow('number', resized_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#pixels = thresholded_image.shape[0]*thresholded_image.shape[1]
#thresholded_image.shape = thresholded_image.reshape(thresholded_image.shape[0], pixels).astype(np.float32)
np.random.seed(seed)
(X_train, y_train), (X_test, y_test) = mnist.load_data()
print(X_train[0].shape)
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype(np.float32)
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype(np.float32)

X_train = X_train / 255
X_test = X_test / 255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

model = baseline_model()
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
scores = model.evaluate(X_test, y_test, verbose=0)
#print(model.predict_on_batch(X_test[0]))
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

#plt.subplot(221)
#plt.imshow(X_train[0], cmap=plt.get_cmap('gray'))
#plt.subplot(222)
#plt.imshow(X_train[1], cmap=plt.get_cmap('gray'))
#plt.subplot(223)
#plt.imshow(X_train[2], cmap=plt.get_cmap('gray'))
#plt.subplot(224)
#plt.imshow(X_train[3], cmap=plt.get_cmap('gray'))

plt.show()



