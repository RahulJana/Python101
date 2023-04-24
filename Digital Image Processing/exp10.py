# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 19:12:36 2020

@author: HP
"""


# erosion
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
erosion = cv.erode(img,kernel,iterations = 1)
cv.imshow('input image',img)
cv.imshow('erosion image',erosion)
cv.waitKey(0)
cv.destroyAllWindows()

# dilation
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
dilation = cv.dilate(img,kernel,iterations = 1)
cv.imshow('input image',img)
cv.imshow('dilation image',dilation)
cv.waitKey(0)
cv.destroyAllWindows()

# opening
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
cv.imshow('input image',img)
cv.imshow('opening image',opening)
cv.waitKey(0)
cv.destroyAllWindows()


# closing
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
cv.imshow('input image',img)
cv.imshow('closing image',closing)
cv.waitKey(0)
cv.destroyAllWindows()


# morphological gradient
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
cv.imshow('input image',img)
cv.imshow('Morphological Gradient image',gradient)
cv.waitKey(0)
cv.destroyAllWindows()


# top hat
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)
cv.imshow('input image',img)
cv.imshow('Top Hat image',tophat)
cv.waitKey(0)
cv.destroyAllWindows()

# black hat
import cv2 as cv
import numpy as np
img = cv.imread('parrots.jpg')
kernel = np.ones((5,5),np.uint8)
blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)
cv.imshow('input image',img)
cv.imshow('Black Hat',blackhat)
cv.waitKey(0)
cv.destroyAllWindows()





















