# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 20:52:28 2020

@author: HP
"""


# Python Program to blur image
# Importing cv2 module
import cv2
# bat.jpg is the batman image.
img = cv2.imread('applications-of-machine-learning.png')
# make sure that you have saved it in the same folder
# You can change the kernel size as you want
blurImg = cv2.blur(img,(5,5))
cv2.imshow('blurred image',blurImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
# image blurring technique called Averaging

# There are some other options available as well – Gaussian Blurring, Median Blurring, Bilateral Filtering.

# Gaussian Blurring
# Again, you can change the kernel size
gausBlur = cv2.GaussianBlur(img, (5,5),0)
cv2.imshow('Gaussian Blurring', gausBlur)
cv2.waitKey(0)
# Median blurring
medBlur = cv2.medianBlur(img,5)
cv2.imshow('Media Blurring', medBlur)
cv2.waitKey(0)
# Bilateral Filtering
bilFilter = cv2.bilateralFilter(img,9,75,75)
cv2.imshow('Bilateral Filtering', bilFilter)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Motion Blur of an image (optional)
# loading library
import cv2
import numpy as np
img = cv2.imread('applications-of-machine-learning.png')
# Specify the kernel size.
# The greater the size, the more the motion.
kernel_size = 30
# Create the vertical kernel.
kernel_v = np.zeros((kernel_size, kernel_size))
# Create a copy of the same for creating the horizontal kernel.
kernel_h = np.copy(kernel_v)
# Fill the middle row with ones.
kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
# Normalize.
kernel_v /= kernel_size
kernel_h /= kernel_size
# Apply the vertical kernel.
vertical_mb = cv2.filter2D(img, -1, kernel_v)
# Apply the horizontal kernel.
horizonal_mb = cv2.filter2D(img, -1, kernel_h)
# Save the outputs.
cv2.imwrite('im_vertical.jpg', vertical_mb)
cv2.imwrite('im_horizontal.jpg', horizonal_mb)
# Display the image
cv2.imshow('im_vertical', vertical_mb)
cv2.imshow('im_horizontal', horizonal_mb)































