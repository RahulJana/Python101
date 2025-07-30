# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:19:22 2020

@author: HP
"""


#Liner Transformation in SD
#Image negative transformation S=(L-1)-r S=(256-1)-r S=255-r
import cv2
img_1= cv2.imread('exp9_pic.jpg',0)
img_2= 255 - img_1
cv2.imshow('input image',img_1)
cv2.imshow('image negative', img_2)
cv2.waitKey(0)
cv2.destroyAllWindows()


#Log Tansformations
#Image log Transformation S=c log(1+r)

import cv2
import numpy as np
img_1= cv2.imread('exp9_pic.jpg',0)
img_2= np.uint8(np.log1p(img_1))
thresh=2
img_3= cv2.threshold(img_2,thresh,255,cv2.THRESH_BINARY)[1]
cv2.imshow('input image',img_1)
cv2.imshow('log transformed image', img_3)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Power law transformation
#S=cr^gamma
import cv2
import numpy as np
img_1= cv2.imread('exp9_pic.jpg',0)
gamma=1
img_2= np.power(img_1,gamma)
gamma=0.7
img_3= np.power(img_1,gamma)
#gamma=4
#img_4= np.power(img_1,gamma)
#gamma=0.7
#img_5= np.power(img_1,gamma)
cv2.imshow('input image',img_1)
cv2.imshow('gamma correction_1', img_2)
cv2.imshow('gamma correction_2', img_3)
#cv2.imshow('gamma correction_3', img_4)
#cv2.imshow('gamma correction_4', img_5)
cv2.waitKey(0)
cv2.destroyAllWindows()