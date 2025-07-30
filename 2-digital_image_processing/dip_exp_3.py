#!/usr/bin/env python
# coding: utf-8

# # Drawing and writing on images using OpenCV 

# In[1]:


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# In[13]:


img = cv.imread('./img1.png', cv.IMREAD_COLOR) 
# drawing line over the image
cv.line(img,(0,0), (150,150), (255,255,0),10)  
cv.imshow('Image window', img) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[6]:


# drawing rectangle over the image
cv.rectangle(img, (100,100), (300,300), (0,0,255), 5) 
cv.imshow('Image window', img) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[9]:


# drawing circle over the image
cv.circle(img, (200,200), 35, (0,214,0), 5)
cv.imshow('Image window', img) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[15]:


# a bunch of points, datatype int32 
ppt = np.array([[10,5], [20,30], [70,20], [110,40]], np.int32)
pts = ppt.reshape((-1,1,2)) 
#pts.shape
cv.polylines(img,(pts), True, (0,0,255), 5) 
cv.imshow('Image window', img) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[17]:


# Writing texts over the image
font = cv.FONT_HERSHEY_SIMPLEX 
cv.putText(img, 'BIHARI',(50,130), font, 1, (120,12,112), 3, cv.LINE_AA ) 
cv.imshow('Image window', img) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[18]:


img_one = cv.imread('img1.png', cv.IMREAD_COLOR) 
# cv.imshow('Image window', img_one) 
# cv.waitKey(0) 
# cv.destroyAllWindows
px = img_one[100,100] 
#BGR at (100,100)
print(px)


# In[19]:


# Changing BGR at (100,100)
img_one[100,100]= [255,255,255]
print(px)


# In[20]:


#Selecting roi 
img_two = cv.imread('img1.png', cv.IMREAD_COLOR)  
px = img_two[100,100] 
img_two[100,100]= [255,255,255]  
roi=img_two[100:120, 100:150] 
print(roi)


# In[21]:


#Selecting BGR and changing its BGR
img_two[100:220, 120:250] = [155,247,157]  
cv.imshow('Image window', img_two) 
cv.waitKey(0) 
cv.destroyAllWindows


# In[22]:


#Selecting a ROI then imposing that roi over some other roi
img_3 = cv.imread('./img2.png', cv.IMREAD_COLOR) 
#px = img_3[200,200] 
#img_3[200,200]= [255,255,255]  
img_3[100:220, 120:250] = [155,247,157] 
nature = img_3[300:350, 120:250]
img_3[0:50,0:130] = nature
cv.imshow('Image window', img_3) 
cv.waitKey(0) 
cv.destroyAllWindows


# # Detecting the colors in an image 

# In[24]:


#Reading in BGR format
image = cv.imread('./naturee.jpg', cv.IMREAD_COLOR)
plt.figure(figsize=(20,8)) 
plt.imshow(image)


# In[25]:


#Converting to RGB formate
RGBimg = cv.cvtColor(image, cv.COLOR_BGR2RGB) 
plt.figure(figsize=(20,8)) 
plt.imshow(RGBimg)


# In[26]:


#Converting RGB to HSV
HSVimg = cv.cvtColor(RGBimg, cv.COLOR_RGB2HSV) 
plt.figure(figsize=(10,10)) 
plt.imshow(HSVimg)


# In[27]:


#Defining the lower bound and upper bound to detect specific color by the help of masking
lower = np.array([10,150,50]) 
upper = np.array([35,255,255]) 
mask = cv.inRange(HSVimg, lower, upper)  
plt.figure(figsize=(20,8)) 
plt.imshow(mask) 


# In[30]:


#Blacken out all other colors leaving HSV part
res=cv.bitwise_and(HSVimg, HSVimg, mask=mask)
plt.figure(figsize=(20,8)) 
plt.imshow(res)


# In[31]:


lower = np.array([35,150,50]) 
upper = np.array([75,255,255]) 
mask = cv.inRange(HSVimg, lower, upper) 
plt.figure(figsize=(20,8)) 
plt.imshow(mask)


# In[41]:


lower = np.array([10,100,100]) 
upper = np.array([75,255,200]) 
mask_1 = cv.inRange(RGBimg, lower, upper) 


# In[43]:


#Blacken out all other colors leaving RGB
res=cv.bitwise_not(RGBimg, RGBimg, mask=mask_1) 
plt.figure(figsize=(20,8)) 
plt.imshow(res)


# In[ ]:




