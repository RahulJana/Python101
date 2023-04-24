# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:07:26 2020

@author: HP
"""


# importing required libraries of opencv
import cv2
# importing library for plotting
from matplotlib import pyplot as plt
# reads an input image
img = cv2.imread('p1.jpg',-1)
plt.imshow(img)
# find frequency of pixels in range 0-255
img = cv2.imread('p1.jpg',0)
histr = cv2.calcHist([img],[0],None,[256],[0,255])
# show the plotting graph of an image
plt.plot(histr)
plt.show()



import cv2
from matplotlib import pyplot as plt
img = cv2.imread('p1.jpg',2)
# alternative way to find histogram of an image
plt.hist(img.ravel(),256,[0,255])
plt.show()


#image pyramid
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("p1.jpg")
layer = img.copy()
for i in range(4):
    plt.subplot(2, 2, i + 1)
    # using pyrDown() function
    layer = cv2.pyrDown(layer)
    plt.imshow(layer)
    cv2.imshow("str(i)", layer)
cv2.waitKey(0)
cv2.destroyAllWindows()

#image translation
import cv2
import numpy as np
image = cv2.imread('p1.jpg')
# Store height and width of the image
height, width = image.shape[:2]
quarter_height, quarter_width = height / 4, width / 4
T = np.float32([[1, 0, quarter_width], [0, 1, quarter_height]])
# We use warpAffine to transform
# the image using the matrix, T
img_translation = cv2.warpAffine(image, T, (width, height))
cv2.imshow("Originalimage", image)
cv2.imshow('Translation', img_translation)
cv2.waitKey()
cv2.destroyAllWindows()
