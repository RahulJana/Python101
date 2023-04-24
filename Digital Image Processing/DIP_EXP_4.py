#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


img1 = cv2.imread('./img1.png') 
img2 = cv2.imread('./img2.png') 


# In[3]:


cv2.imshow('img1',img1) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# In[4]:


cv2.imshow('img2',img2) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# In[7]:


add = img1+img2 
cv2.imshow('addition window',add) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


# In[6]:


img1 = cv2.imread('./img1.png') 
img2 = cv2.imread('./img2.png') 
add = cv2.add(img1,img2) 
cv2.imshow('addition window',add) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[ ]:


weighted = cv2.addWeighted(img1, 0.6, img2, 0.4, 1)
cv2.imshow('add weighted window',weighted) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# # Performing bitwise operation using mask_inverse

# In[8]:


img1 = cv2.imread('./img2.png') 
img2 = cv2.imread('./python-logo.png') 
cv2.imshow('img2', img2) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[9]:


cv2.imshow('img1', img1) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[10]:


rows,cols,channels = img2.shape 
roi = img1[0:cols, 0:rows] 


# In[11]:


img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
cv2.imshow('img2gray',img2gray) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[12]:


ret, mask = cv2.threshold(img2gray, 250, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('mask window', mask) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[13]:


mask_inv = cv2.bitwise_not(mask) 
cv2.imshow('inverse mask window', mask_inv) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[14]:


img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
cv2.imshow('blackout area in roi', img1_bg) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[15]:


img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
cv2.imshow('take out region of logo from logo image', img2_fg) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[16]:


dst = cv2.add(img1_bg,img2_fg) 
cv2.imshow('dst window', dst) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[17]:


img1[0:cols, 0:rows ] = dst 
cv2.imshow('result', img1) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


# In[ ]:




