#!/usr/bin/env python
# coding: utf-8

# # <font colour = "red">Python : Reading and dipalying the image using different modules</font>

# ## <font colour = "green">Method 1</font>
# ## <font colour = "blue">Using Pillow (PIL) module</font>

# In[1]:


# Importing PIL Module
from PIL import Image

# Read Image, which is in the same foulder
img = Image.open('./morali.jpg')

# Display the Image
img.show()


# ## <font colour = "green">Mentod 1.2</font>
# ## <font colour = "blue">Using Pillow (PIL) with matplotlib module</font>
# 

# In[2]:


# Importing PIL Module
from PIL import Image
# Importing Matplotlib module
import matplotlib.pyplot as plt

# Read Image, which is in the same foulder
img = plt.imread('./lena image.jpg')
# using matplotlib to display the image
plt.imshow(img)


# ## <font colour = "green">Mentod 2</font>
# ## <font colour = "blue">Using Matplotlib module</font>

# In[20]:


#Importing Matplotlib Module
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Read the Image , which is in the same foulder
img = mpimg.imread('./morali.jpg')

# Displaying the image using matplotlib
plt.imshow(img)


# ## <font colour = "green">Mentod 3</font>
# ## <font colour = "blue">Using imageio with matplotlib module</font>

# In[4]:


#Importing imageio module
import imageio
# Importing matplotlib module
import matplotlib.pyplot as plt

# Read the image using imageio
img = imageio.imread('./lena image.jpg')

# Display the image using imageio
plt.imshow(img)


# ## <font colour = "green">Mentod 4</font>
# ## <font colour = "blue">Using OpenCV module</font>

# In[16]:


# Import OpenCV-Python (cv2) Module
import cv2 as cv
# Read the Image
img = cv.imread('./morali.jpg',1)
# NB: 1 IMREAD_COLOUR IMAGE, NB:0 IMREAD_ GREYSCALE IMAGE, NB:-1 IMREAD_UNCHANGE IMAGE

# Display the image using openCV
cv.imshow('windowTitle', img)

# Display the image until you press any key
cv.waitKey(0)


# ## <font colour = "green">Mentod 5</font>
# ## <font colour = "blue">Using OpenCV with Matplotlib module</font>

# In[19]:


# Import OpenCV-Python (cv2) Module
import cv2 as cv
# Importing Matplotlib Module
import matplotlib.pyplot as plt

# Read the Image in greyscale
img = cv.imread('./morali.jpg',-1)
# NB: 1 IMREAD_COLOUR IMAGE, NB:0 IMREAD_ GREYSCALE IMAGE, NB:-1 IMREAD_UNCHANGE IMAGE

# Convert GBR colour mode to RGB colour mode
RGBimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# using matplotlib to display the image
plt.imshow(RGBimg)


# In[15]:


# Import OpenCV-Python (cv2) Module
import cv2 as cv
# Importing Matplotlib Module
import matplotlib.pyplot as plt

# Read the Image in greyscale
img = cv.imread('./morali.jpg',1)
# NB: 1 IMREAD_COLOUR IMAGE, NB:0 IMREAD_ GREYSCALE IMAGE, NB:-1 IMREAD_UNCHANGE IMAGE
#using matplotlib to display the image
plt.imshow(img)


# In[ ]:




