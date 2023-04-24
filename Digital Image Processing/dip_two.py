#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import cv2 


# In[2]:


img = cv2.imread('./img1.png', cv2.IMREAD_GRAYSCALE)

# we can use IMREAD_GRAYSCALE for colour image instead of 0
# we can use IMREAD_COLOR for colour image instead of 1
# we can use IMREAD_UNCHANGE for colour image instead of -1

# Displaying the image
cv2.imshow('Image window', img)

cv2.waitKey(0)
cv2.destroyAllWindows


# In[14]:


img = cv2.imread('./img2.png',1)

# we can use IMREAD_GRAYSCALE for colour image instead of 0
# we can use IMREAD_COLOR for colour image instead of 1
# we can use IMREAD_UNCHANGE for colour image instead of -1

# Displaying the image using matplotlib module
#plt.imshow(img, cmap='gray', intrepolation='bicubic')
#plt.show()

# Convert GBR colour mode to RGB colour mode
RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# To plot on the image
plt.plot([100,400] , [230,400] ,'r' , linewidth=10)
#[x1,x2] [y1,y2]
# using matplotlib to display the image
plt.imshow(RGBimg)

# Save the image
# cv2.imwrite('./ flute.png' , img)


# In[15]:


cap = cv2.VideoCapture(".\dip_video.mp4")
 
while(True):
    
    #infinite loop, ret_repeat
    ret, frame = cap.read()
    # To display the video
    cv2.imshow('frame Window',frame)
    # To be broken later by a break statement
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break


cap.release()
cv2.destroyAllWindows()


# In[10]:


cap = cv2.VideoCapture(".\dip_video.mp4")
 
while(True):
    
    #infinite loop, ret_repeat
    ret, frame = cap.read()
    #convering to gray
    grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # To display the video
    cv2.imshow('frame Window',frame)
    cv2.imshow('Gray Window', grayimg)
    # To be broken later by a break statement
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:




