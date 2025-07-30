#!/usr/bin/env python
# coding: utf-8

# # Experiment-2 (OpenCV with Python for Image and Video Analysis) 

# ## Method 1.0: Reading an image using cv2

# In[1]:


# Importing required modules
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Defining and reading an Image usinig opencv module
img = cv.imread('./morali.jpg', cv.IMREAD_GRAYSCALE)

# we can use IMREAD_GRAYSCALE for colour image instead of 0
# we can use IMREAD_COLOR for colour image instead of 1
# we can use IMREAD_UNCHANGE for colour image instead of -1

# Displaying the image
cv.imshow('Image window', img)

cv.waitKey(0)
cv.destroyAllWindows


# # Method 1.1: Reading , displaying and ploting the image using matplotlib in cv2.

# In[8]:


# Importing required modules
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Defining and reading an Image usinig opencv module
img = cv.imread('./morali.jpg', cv.IMREAD_GRAYSCALE)

# we can use IMREAD_GRAYSCALE for colour image instead of 0
# we can use IMREAD_COLOR for colour image instead of 1
# we can use IMREAD_UNCHANGE for colour image instead of -1

# Displaying the image using matplotlib module
#plt.imshow(img, cmap='gray', intrepolation='bicubic')
#plt.show()

# Convert GBR colour mode to RGB colour mode
RGBimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# To plot on the image
plt.plot([120,700] , [230,700] , 'c' , linewidth=5)

# using matplotlib to display the image
plt.imshow(RGBimg)

# Save the image
cv.imwrite('./ flute.png' , img)


# # Method 1.2: Reading the imageand saving it.

# In[18]:


# Importing required modules
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Defining and reading an Image usinig opencv module
img = cv.imread('./morali.jpg', cv.IMREAD_GRAYSCALE)

# we can use IMREAD_GRAYSCALE for colour image instead of 0
# we can use IMREAD_COLOR for colour image instead of 1
# we can use IMREAD_UNCHANGE for colour image instead of -1

# Displaying the image
cv.imshow('Image window', img)

cv.waitKey(0)
cv.destroyAllWindows


# Save the image
cv.imwrite('./flute.png' , img)


# # Working with video Source 
# 
# ## Method 2.0: Capture the video 

# In[4]:


# Importing required modules
import numpy as np
import cv2 as cv

# To capture the video
cap = cv.VideoCapture('./video.mp4')
 
while(True):
    
    #infinite loop, ret_repeat
    ret, frame = cap.read()
    # To display the video
    cv.imshow('frame Window',frame)
    # To be broken later by a break statement
    if cv.waitKey(1) & 0xFF == ord('1'):
        break


cap.release()
cv.destroyAllWindows()


# ## Method 2.1:  Capture and displaying the video in gray scale

# In[7]:


# Importing required modules
import numpy as np
import cv2 as cv

cap = cv.VideoCapture('./video.mp4')
 
while(True):
    
    #infinite loop, ret_repeat
    ret, frame = cap.read()
    #convering to gray
    grayimg = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # To display the video
    cv.imshow('frame Window',frame)
    cv.imshow('Gray Window', grayimg)
    # To be broken later by a break statement
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


# In[ ]:




