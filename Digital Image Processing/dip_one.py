#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image

img = Image.open('./img2.png')

img.show()


# In[3]:


from PIL import Image
import matplotlib.pyplot as plt
img = plt.imread('./img1.png')
plt.imshow(img)


# In[4]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('./murali.png')
plt.imshow(img)


# In[5]:


import imageio
import matplotlib.pyplot as plt
img = imageio.imread('./img2.png')
plt.imshow(img)


# In[10]:


import cv2
img = cv2.imread('./img2.png',-1)
cv2.imshow('windowTitle', img)
cv2.waitKey(0)


# In[11]:


img_two = cv2.imread('./img2.png',-1)
plt.imshow(img_two)
RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(RGBimg)


# In[12]:


# Read the Image in greyscale
img = cv2.imread('./img2.png',1)
# NB: 1 IMREAD_COLOUR IMAGE, NB:0 IMREAD_ GREYSCALE IMAGE, NB:-1 IMREAD_UNCHANGE IMAGE
#using matplotlib to display the image
plt.imshow(img)


# In[ ]:




